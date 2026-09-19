# 🤖 CrewAI GitHub Repository Summarizer

A Streamlit application that accepts a **GitHub username** and uses a **CrewAI multi-agent workflow** with a **Groq LLM** to research and summarize public repositories.

## Important fix included

If you received this error:

```text
GroqException:
'messages.0': for 'role:system' the following must be satisfied
[('messages.0': property 'cache_breakpoint' is unsupported)]
```

this project already contains a compatibility patch in `config.py`.

This is a known CrewAI/Groq compatibility issue in affected CrewAI releases: CrewAI can inject `cache_breakpoint` into messages, while Groq rejects that field. The patch disables that injection before the Groq request.

Groq's API accepts standard chat-completion messages but does not accept that unsupported message property. See the current Groq API documentation and the documented CrewAI issue for details.

## CrewAI concepts demonstrated

### Agents
1. GitHub Repository Researcher
2. Technical Repository Analyst
3. Repository Summary Writer

### Tools
1. `github_user_repositories`
2. `github_repository_details`

### Tasks
1. Repository research
2. Technical analysis
3. Final summarization

The workflow is sequential:

```text
GitHub Username
      ↓
Streamlit
      ↓
CrewAI
      ↓
Research Agent
      ↓
GitHub Tools
      ↓
Technical Analyst
      ↓
Summary Writer
      ↓
Groq LLM
      ↓
Final Repository Report
```

## Setup

### 1. Extract the ZIP

Open the extracted project folder in VS Code.

### 2. Create virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
venv\Scripts\activate.bat
```

### 3. Install packages

```powershell
pip install -r requirements.txt
```

### 4. Create `.env`

Copy `.env.example` to `.env`:

```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=groq/llama-3.3-70b-versatile

or====>
HF_TOKEN="put your Hugging Face token here"
HF_MODEL=openai/gpt-oss-120b
```

Do not upload `.env` to GitHub.

### 5. Run

```powershell
streamlit run app.py
```

Then enter a public GitHub username such as:

```text
saurav526
```

and click:

```text
🚀 Analyze Repositories
```

## If you still get a `cache_breakpoint` error

Make sure the application is running from the updated project folder and that the virtual environment is active.

Then run:

```powershell
pip show crewai
```

and:

```powershell
python -c "import crewai; print(crewai.__version__)"
```

Restart Streamlit after changing packages:

```powershell
streamlit run app.py
```

## Project files

```text
crew_github_repo_summarizer/
│
├── app.py
├── agents.py
├── tasks.py
├── tools.py
├── config.py          ← Groq compatibility patch
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## What happens internally

### Agent 1 — GitHub Repository Researcher

Uses the GitHub tools to retrieve:
- repository name
- URL
- description
- language
- stars
- forks
- topics
- README

### Agent 2 — Technical Repository Analyst

Receives the research and explains:
- project purpose
- technologies
- architecture/workflow
- important features
- presentation-friendly explanation

### Agent 3 — Repository Summary Writer

Combines the previous outputs into a structured Markdown report.

The project therefore demonstrates **Agents + Tools + Tasks**, not just a single LLM call.

## Notes

- Only public GitHub information is used.
- The GitHub API is accessed directly by the CrewAI tools.
- The LLM is Groq.
- Streamlit is the frontend.
- The application does not require a GitHub token for public repositories.
