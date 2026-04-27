import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


load_dotenv()

def get_llm(temperature: float = 0):
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=temperature,
    )
