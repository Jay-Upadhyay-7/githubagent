from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage
from crewai import Agent, Task, Crew, Process
from backend.app.agents.agents import GitHubAgents

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    repo_url: str
    analysis_result: str
    impact_result: str

agents = GitHubAgents()
analyst = agents.commit_analyst()
assessor = agents.impact_assessor()

def analyze_commits(state: AgentState):
    repo_url = state['repo_url']
    
    # Get current Langfuse handler
    try:
        from langfuse import langfuse_context
        handler = langfuse_context.get_current_langchain_handler()
        # Set callbacks for the agent's LLM
        if analyst.llm:
            analyst.llm.callbacks = [handler]
    except Exception as e:
        print(f"Failed to set Langfuse callback: {e}")

    task = Task(
        description=f"Analyze the last 5 commits of the repository at {repo_url}. Summarize the changes.",
        agent=analyst,
        expected_output="A detailed summary of the recent changes."
    )
    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=True
    )
    result = crew.kickoff()
    return {"analysis_result": str(result)}

def assess_impact(state: AgentState):
    repo_url = state['repo_url']
    analysis = state['analysis_result']

    # Get current Langfuse handler
    try:
        from langfuse import langfuse_context
        handler = langfuse_context.get_current_langchain_handler()
        # Set callbacks for the agent's LLM
        if assessor.llm:
            assessor.llm.callbacks = [handler]
    except Exception as e:
        print(f"Failed to set Langfuse callback: {e}")

    task = Task(
        description=f"Based on the following analysis of recent commits: {analysis}, assess the impact on the main branch and suggest any necessary updates or precautions.",
        agent=assessor,
        expected_output="An impact assessment report."
    )
    crew = Crew(
        agents=[assessor],
        tasks=[task],
        verbose=True
    )
    result = crew.kickoff()
    return {"impact_result": str(result)}

workflow = StateGraph(AgentState)

workflow.add_node("analyze", analyze_commits)
workflow.add_node("assess", assess_impact)

workflow.set_entry_point("analyze")
workflow.add_edge("analyze", "assess")
workflow.add_edge("assess", END)

app = workflow.compile()
