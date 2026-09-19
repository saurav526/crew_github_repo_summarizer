from crewai import Agent
from tools import github_user_repositories, github_repository_details
from config import get_llm

def create_agents():
    llm = get_llm()

    github_researcher = Agent(
        role="GitHub Repository Researcher",
        goal="Find and collect accurate information about a GitHub user's public repositories.",
        backstory=(
            "You are an expert GitHub researcher. You inspect public repository metadata, "
            "README files, languages, topics, stars, forks, and activity. "
            "You never invent repository information."
        ),
        tools=[github_user_repositories, github_repository_details],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    technical_analyst = Agent(
        role="Technical Repository Analyst",
        goal="Understand the technical purpose, architecture, technologies, and practical use of each repository.",
        backstory=(
            "You are a senior software and AI engineer. You convert raw GitHub repository "
            "information into concise technical explanations suitable for a student portfolio."
        ),
        tools=[github_repository_details],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    summarizer = Agent(
        role="Repository Summary Writer",
        goal="Produce a clear final summary of the user's repositories without hallucinating facts.",
        backstory=(
            "You are a technical writer who creates structured, readable repository summaries. "
            "You clearly distinguish available information from information that could not be found."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    return {
        "researcher": github_researcher,
        "analyst": technical_analyst,
        "summarizer": summarizer,
    }
