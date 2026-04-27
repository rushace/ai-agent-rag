import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    session_id: str

class DocumentAgentInput(BaseModel):
    query: str
    task: str  # summarize | qa | extract


class DocumentAgentOutput(BaseModel):
    answer: str
    citations: List[str]


class LegalResearchInput(BaseModel):
    query: str
    needs_statute: bool = False
    needs_case_law: bool = False
    needs_web: bool = False


class LegalResearchOutput(BaseModel):
    analysis: str
    acts: List[str] = []
    cases: List[str] = []
    web: List[str] = []

class DrafterInput(BaseModel):
    document_type: str
    facts: str
    legal_basis: str


class DrafterOutput(BaseModel):
    draft: str

