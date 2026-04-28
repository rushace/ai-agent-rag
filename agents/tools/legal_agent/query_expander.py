
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))



from pydantic import BaseModel
from typing import List
from shared.prompts import QUERY_EXPANDER_PROMPT
from shared.llm import get_llm_secondary,get_llm_primary
from .query_processor import ParsedQuery

class ExpandedQueries(BaseModel):
    queries: List[str]



def get_query_expansion_chain():
    llm = get_llm_secondary(temperature=0.2)  # slight creativity
    return QUERY_EXPANDER_PROMPT | llm.with_structured_output(ExpandedQueries)


def expand_queries(parsed_query: ParsedQuery) -> List[str]:
    try:
        chain = get_query_expansion_chain()

        result = chain.invoke({
            "query": parsed_query.clean_query,
            "clean_query": parsed_query.clean_query,
            "section_number": parsed_query.section_number,
            "act": parsed_query.act
        })

        queries = result.queries

        if not queries or len(queries) < 2:
            raise ValueError("Weak expansion")

        return queries

    except Exception:
        # fallback
        return [parsed_query.clean_query]

def clean_queries(queries: list[str]) -> list[str]:
    unique = list(dict.fromkeys(q.strip() for q in queries))
    return unique[:5]


# # testing 
# if __name__ == "__main__":
#     from query_processor import analyze_query

#     parsed = analyze_query("Explain section 5 of cantonment act")
#     queries = expand_queries(parsed)
#     print("\nExpanded Queries:")
#     for q in queries:
#         print("-", q)