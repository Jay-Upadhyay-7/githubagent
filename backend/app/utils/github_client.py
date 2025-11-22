import os
from github import Github
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GitHubClient:
    def __init__(self, token: str = None):
        self.token = token or os.getenv("GITHUB_ACCESS_TOKEN")
        if not self.token:
            raise ValueError("GitHub token is required")
        self.g = Github(self.token)

    def get_repo(self, repo_url: str):
        # Extract owner and repo name from URL
        # Example: https://github.com/owner/repo
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise ValueError("Invalid GitHub URL")
        owner = parts[-2]
        repo_name = parts[-1]
        return self.g.get_repo(f"{owner}/{repo_name}")

    def get_recent_commits(self, repo_url: str, limit: int = 10) -> List[Dict[str, Any]]:
        repo = self.get_repo(repo_url)
        commits = repo.get_commits()[:limit]
        result = []
        for commit in commits:
            result.append({
                "sha": commit.sha,
                "message": commit.commit.message,
                "author": commit.commit.author.name,
                "date": commit.commit.author.date.isoformat(),
                "url": commit.html_url
            })
        return result

    def get_commit_diff(self, repo_url: str, sha: str) -> str:
        repo = self.get_repo(repo_url)
        commit = repo.get_commit(sha)
        files_changed = []
        for file in commit.files:
            files_changed.append(f"File: {file.filename}\nStatus: {file.status}\nPatch:\n{file.patch}")
        return "\n\n".join(files_changed)

    def get_branches(self, repo_url: str) -> List[str]:
        repo = self.get_repo(repo_url)
        return [branch.name for branch in repo.get_branches()]
