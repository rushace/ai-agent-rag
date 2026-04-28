# query_processor.py


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))


from pydantic import BaseModel
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from shared.llm import get_llm_secondary,get_llm_primary
from shared.prompts import QUERY_ANALYZER_PROMPT
from rich import print

class ParsedQuery(BaseModel):
    clean_query: str
    section_number: Optional[str] = None
    act: Optional[str] = None
    intent: str





def get_query_parser_chain():
    llm = get_llm_primary(temperature=0)
    return QUERY_ANALYZER_PROMPT | llm.with_structured_output(ParsedQuery)


def analyze_query(query: str) -> ParsedQuery:
    chain = get_query_parser_chain()
    result = chain.invoke({"query": query})
    return result

