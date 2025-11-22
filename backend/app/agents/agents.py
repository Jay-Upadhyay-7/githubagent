from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from backend.app.tools.github_tool import fetch_recent_commits, fetch_commit_diff

# Wrap tools if necessary or ensure they are passed correctly
# In recent CrewAI versions, LangChain tools are supported but sometimes Pydantic validation fails.
# Let's try to use them directly first, but if that fails (which it did), we might need to check imports.
# The error was "Input should be a valid dictionary or instance of BaseTool".
# This often happens if the tool is not recognized as a BaseTool.
# Let's try to explicitly cast or wrap them if needed. 
# However, the previous error showed they were StructuredTool.
# Let's try to use the `tools` argument with a list of functions if they are decorated with @tool? 
# No, they need to be tool instances.

# Let's try to re-import and see if we can define them differently in github_tool.py
# For now, I will assume the issue is Pydantic v2.


class GitHubAgents:
    def commit_analyst(self):
        return Agent(
            role='Commit Analyst',
            goal='Analyze code changes in GitHub commits and provide a technical summary.',
            backstory='You are an expert software engineer who specializes in code review and understanding complex codebases. You can read diffs and explain what changed in plain English.',
            tools=[fetch_recent_commits, fetch_commit_diff],
            verbose=True,
            allow_delegation=False
        )

    def impact_assessor(self):
        return Agent(
            role='Impact Assessor',
            goal='Evaluate the impact of code changes on the main branch and suggest updates.',
            backstory='You are a senior DevOps engineer and architect. You understand system dependencies and can predict how changes in one part of the code might affect others. You focus on stability and performance.',
            tools=[fetch_recent_commits, fetch_commit_diff],
            verbose=True,
            allow_delegation=False
        )

    def planner(self):
        return Agent(
            role='Project Planner',
            goal='Help developers plan future tasks based on recent commits and leftover work.',
            backstory='You are a technical project manager. You keep track of what has been done and what needs to be done. You facilitate collaboration between developers.',
            verbose=True,
            allow_delegation=True
        )
