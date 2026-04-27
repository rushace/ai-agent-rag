import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

#     query = query.lower()

#     if "bail" in query:
#         return "bail_application"
#     elif "notice" in query:
#         return "legal_notice"

#     return "general_document"
def extract_document_type(query: str) -> str:
    query = query.lower()

    if "bail" in query:
        return "bail_application"
    elif "notice" in query:
        return "legal_notice"
    elif "petition" in query:
        return "petition"
    
    return "general_legal_document"

def extract_facts(query: str) -> str:
    return f"Case Details: {query}"