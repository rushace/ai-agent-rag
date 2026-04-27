import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.models import DocumentAgentInput, DocumentAgentOutput

def document_intelligence_agent(input_data: DocumentAgentInput) -> DocumentAgentOutput:
    return DocumentAgentOutput(
        answer=f"[DOC] Processed query: {input_data.query}",
        citations=["doc1", "doc2"]
    )