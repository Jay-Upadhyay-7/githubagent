# GitHub Agentic Application

An intelligent, agent-powered application that monitors GitHub repositories, analyzes commits, and provides actionable insights using advanced AI workflows.

## 🚀 Key Features & Technologies

### 🤖 CrewAI Agents
We employ a team of specialized AI agents working in harmony:
- **Commit Analyst**: Fetches and interprets raw commit data, turning technical diffs into human-readable summaries.
- **Impact Assessor**: Evaluates the risk level of changes, ensuring main branch stability.
- **Project Planner**: Assists developers in planning next steps based on the current codebase state.

### 🕸️ LangGraph Orchestration
The application's brain is built on **LangGraph**, which manages the stateful workflow between agents. It ensures a structured flow of data:
`Input URL` -> `Analysis` -> `Impact Assessment` -> `User Report`.

### 🔭 Langfuse Observability
Integrated **Langfuse** tracing provides complete visibility into the AI's decision-making process. You can monitor:
- Full LLM traces and prompts.
- Latency and cost per execution.
- Agent tool usage and outputs.


## 🚀 Quick Start

### Prerequisites
-   Python 3.10+
-   Node.js 18+
-   Git

### 1. Environment Variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```
Required: `GITHUB_ACCESS_TOKEN`, `OPENAI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`.

### 2. Start Backend
```bash
# In root directory
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```
-   **API**: `http://localhost:8000`
-   **Swagger UI**: `http://localhost:8000/docs`

### 3. Start Frontend
```bash
# In frontend directory
cd frontend
npm install
npm run dev
```
-   **Dashboard**: `http://localhost:3000`

## 🧪 Testing
Run backend tests:
```bash
pytest backend/tests
```
