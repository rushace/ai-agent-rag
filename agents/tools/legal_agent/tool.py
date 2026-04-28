import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from langchain.tools import tool
from pipeline import legal_rag_pipeline


@tool("legal_research_tool")
def legal_research_tool(query: str) -> str:
    """
    Performs legal research using bare acts and legal database.
    """

    result = legal_rag_pipeline(query)

    return result["answer"]