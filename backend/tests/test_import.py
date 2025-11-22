import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from app.main import app
    from app.utils.github_client import GitHubClient
    from app.agents.agents import GitHubAgents
    from app.core.graph import workflow
    print("Imports successful!")
except Exception as e:
    print(f"Import failed: {e}")
    sys.exit(1)
