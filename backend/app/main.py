from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.app.core.graph import app as graph_app
from langfuse import observe

app = FastAPI(title="GitHub Agentic App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    repo_url: str

@app.post("/analyze")
@observe()
async def analyze_repo(request: AnalyzeRequest):
    try:
        inputs = {"repo_url": request.repo_url, "messages": []}
        result = graph_app.invoke(inputs)
        return {
            "analysis": result.get("analysis_result"),
            "impact": result.get("impact_result")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
@observe()
async def chat(request: ChatRequest):
    # Simple chat implementation using the planner agent directly or via graph
    # For now, we'll just echo or use a simple response since the graph is focused on analysis.
    # Ideally, we should have a separate graph or branch for chat.
    # Let's use the Planner agent directly for now.
    try:
        from backend.app.agents.agents import GitHubAgents
        from crewai import Task, Crew
        
        agents = GitHubAgents()
        planner = agents.planner()
        
        task = Task(
            description=f"User says: {request.message}. Respond helpfully regarding the project plan or code changes.",
            agent=planner,
            expected_output="A helpful response to the user."
        )
        
        crew = Crew(
            agents=[planner],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        return {"response": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to GitHub Agentic App API"}

