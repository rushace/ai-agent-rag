# Ai Agent Creation and testing 


from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from rich import print


load_dotenv()


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

llm = ChatGroq(model="llama-3.1-8b-instant",api_key=os.getenv("GROQ_API_KEY"))

agent = create_agent(llm, tools=[get_weather])
# Test the agent

response = agent.invoke(
    {
        "messages": [("user", "What's the weather like in New York?")]
    }
)
print(response["messages"][-1].content)


