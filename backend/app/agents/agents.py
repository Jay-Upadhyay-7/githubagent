from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from backend.app.tools.github_tool import fetch_recent_commits, fetch_commit_diff


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
