from crewai import Task

def create_tasks(username, max_repos, agents):
    research_task = Task(
        description=f"""
        Research the public GitHub repositories belonging to the user "{username}".

        Analyze at most {max_repos} repositories, prioritizing repositories that contain
        useful public information.

        For each repository collect:
        - repository name and URL
        - description
        - primary language and visible technologies
        - stars and forks when available
        - topics when available
        - README information
        - important files or project structure when available
        - what the project appears to do

        Use the GitHub tools rather than guessing.
        """,
        expected_output="A factual dataset-like research report containing one section per repository.",
        agent=agents["researcher"],
    )

    analysis_task = Task(
        description="""
        Using the GitHub research produced by the previous task, technically analyze every
        repository.

        For each repository explain:
        1. Project purpose
        2. Main technologies
        3. Likely workflow/architecture based only on available evidence
        4. Key features
        5. A simple explanation a BTech student could use in a presentation

        Do not invent implementation details that are not supported by repository evidence.
        """,
        expected_output="A technical analysis for every researched repository.",
        agent=agents["analyst"],
        context=[research_task],
    )

    summary_task = Task(
        description="""
        Create the final answer for the user.

        Format it as:

        # GitHub Profile Repository Analysis

        ## Profile
        Username and total repositories analyzed.

        ## Repository 1 — <name>
        - URL:
        - Purpose:
        - Technologies:
        - Key features:
        - Technical workflow:
        - Short presentation explanation:

        Repeat for every repository.

        ## Overall Profile Summary
        Give a neutral summary of the technologies and project categories visible across
        the analyzed repositories.

        Keep the output clear and useful. Never claim something that was not supported
        by the research.
        """,
        expected_output="A polished Markdown report covering every analyzed repository.",
        agent=agents["summarizer"],
        context=[research_task, analysis_task],
    )

    return [research_task, analysis_task, summary_task]
