import streamlit as st
from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks

st.set_page_config(page_title="GitHub Repo Summarizer", page_icon="🤖", layout="wide")

st.title("🤖 GitHub User Repository Summarizer")
st.write("Enter a GitHub username and let a CrewAI multi-agent workflow analyze and summarize their public repositories.")

username = st.text_input("GitHub Username", placeholder="e.g. saurav526")
max_repos = st.slider("Maximum repositories to analyze", min_value=1, max_value=15, value=5)

if st.button("🚀 Analyze Repositories", type="primary"):
    if not username.strip():
        st.error("Please enter a GitHub username.")
        st.stop()

    with st.spinner("Creating CrewAI agents and analyzing repositories..."):
        try:
            agents = create_agents()
            tasks = create_tasks(username.strip(), max_repos, agents)

            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True,
            )

            result = crew.kickoff()

            st.success("Analysis completed!")
            st.subheader("📊 Repository Summary")
            st.markdown(str(result))

        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info(
    "Check your HF_TOKEN and HF_MODEL in the .env file, "
    "and make sure the GitHub username is valid."
)

st.divider()
st.caption("Built with CrewAI + Groq + GitHub REST API + Streamlit")
