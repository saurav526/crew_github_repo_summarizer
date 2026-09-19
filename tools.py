import requests
from crewai.tools import tool

GITHUB_API = "https://api.github.com"


def _headers():
    return {
        "Accept": "application/vnd.github+json",
        "User-Agent": "CrewAI-GitHub-Repository-Summarizer"
    }


@tool("github_user_repositories")
def github_user_repositories(username: str) -> str:
    """Fetch public repositories for a GitHub username."""
    url = f"{GITHUB_API}/users/{username}/repos"
    params = {"per_page": 100, "sort": "updated"}
    response = requests.get(url, headers=_headers(), params=params, timeout=20)

    if response.status_code == 404:
        return f"GitHub user '{username}' was not found."

    response.raise_for_status()
    repos = response.json()

    if not repos:
        return f"No public repositories found for '{username}'."

    lines = []
    for repo in repos:
        lines.append(
            f"NAME: {repo.get('name')}\n"
            f"URL: {repo.get('html_url')}\n"
            f"DESCRIPTION: {repo.get('description')}\n"
            f"LANGUAGE: {repo.get('language')}\n"
            f"STARS: {repo.get('stargazers_count')}\n"
            f"FORKS: {repo.get('forks_count')}\n"
            f"TOPICS: {', '.join(repo.get('topics') or [])}\n"
            f"DEFAULT_BRANCH: {repo.get('default_branch')}\n"
        )

    return "\n---\n".join(lines)


@tool("github_repository_details")
def github_repository_details(repository_url: str) -> str:
    """Fetch detailed metadata and README content for a public GitHub repository URL."""
    parts = repository_url.rstrip("/").split("/")
    if len(parts) < 2:
        return "Invalid GitHub repository URL."

    owner, repo = parts[-2], parts[-1]
    repo_api = f"{GITHUB_API}/repos/{owner}/{repo}"

    response = requests.get(repo_api, headers=_headers(), timeout=20)
    if response.status_code == 404:
        return f"Repository '{owner}/{repo}' was not found."

    response.raise_for_status()
    data = response.json()

    readme_url = f"{GITHUB_API}/repos/{owner}/{repo}/readme"
    readme_response = requests.get(readme_url, headers=_headers(), timeout=20)

    readme = "README not available."
    if readme_response.ok:
        readme_data = readme_response.json()
        import base64
        try:
            readme = base64.b64decode(readme_data.get("content", "")).decode("utf-8", errors="ignore")
        except Exception:
            readme = "README could not be decoded."

    # Keep tool output reasonably sized for the LLM.
    readme = readme[:12000]

    return (
        f"Repository: {data.get('full_name')}\n"
        f"URL: {data.get('html_url')}\n"
        f"Description: {data.get('description')}\n"
        f"Language: {data.get('language')}\n"
        f"Stars: {data.get('stargazers_count')}\n"
        f"Forks: {data.get('forks_count')}\n"
        f"Topics: {', '.join(data.get('topics') or [])}\n"
        f"Default branch: {data.get('default_branch')}\n"
        f"Created: {data.get('created_at')}\n"
        f"Last updated: {data.get('updated_at')}\n\n"
        f"README:\n{readme}"
    )
