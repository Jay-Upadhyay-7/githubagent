from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from backend.app.utils.github_client import GitHubClient

github_client = GitHubClient()

class FetchRecentCommitsInput(BaseModel):
    repo_url: str = Field(..., description="The URL of the GitHub repository")
    limit: int = Field(10, description="The number of commits to fetch")

class FetchRecentCommitsTool(BaseTool):
    name: str = "fetch_recent_commits"
    description: str = "Fetches the recent commits from a GitHub repository."
    args_schema: Type[BaseModel] = FetchRecentCommitsInput

    def _run(self, repo_url: str, limit: int = 10) -> str:
        try:
            commits = github_client.get_recent_commits(repo_url, limit)
            return str(commits)
        except Exception as e:
            return f"Error fetching commits: {str(e)}"

class FetchCommitDiffInput(BaseModel):
    repo_url: str = Field(..., description="The URL of the GitHub repository")
    sha: str = Field(..., description="The SHA hash of the commit")

class FetchCommitDiffTool(BaseTool):
    name: str = "fetch_commit_diff"
    description: str = "Fetches the diff (changes) of a specific commit."
    args_schema: Type[BaseModel] = FetchCommitDiffInput

    def _run(self, repo_url: str, sha: str) -> str:
        try:
            diff = github_client.get_commit_diff(repo_url, sha)
            return diff
        except Exception as e:
            return f"Error fetching diff: {str(e)}"

class FetchBranchesInput(BaseModel):
    repo_url: str = Field(..., description="The URL of the GitHub repository")

class FetchBranchesTool(BaseTool):
    name: str = "fetch_branches"
    description: str = "Fetches the list of branches in a GitHub repository."
    args_schema: Type[BaseModel] = FetchBranchesInput

    def _run(self, repo_url: str) -> str:
        try:
            branches = github_client.get_branches(repo_url)
            return str(branches)
        except Exception as e:
            return f"Error fetching branches: {str(e)}"

fetch_recent_commits = FetchRecentCommitsTool()
fetch_commit_diff = FetchCommitDiffTool()
fetch_branches = FetchBranchesTool()
