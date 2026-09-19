import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


def get_llm():

    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        raise ValueError(
            "HF_TOKEN is missing. Add it to your .env file."
        )

    return LLM(
        model="openai/gpt-oss-120b",
        api_key=hf_token,
        base_url="https://router.huggingface.co/v1",
        temperature=0.2,
    )