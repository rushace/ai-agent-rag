from enum import Enum
from pydantic import BaseModel,Field
from typing import List, Dict, Any, Optional

class IntentType(str, Enum):
    DOC_ANALYSIS = "DOC_ANALYSIS"
    LEGAL_RESEARCH = "LEGAL_RESEARCH"
    DRAFTING = "DRAFTING"
    HYBRID = "HYBRID"

class PlanStep(BaseModel):
    agent: str
    task: str

class SupervisorState(BaseModel):
    query: str
    intent: Optional[IntentType] = None
    plan: List[PlanStep] = Field(default_factory=list)
    intermediate_results: List[Dict[str, Any]] = Field(default_factory=list)
    final_output: Optional[str] = None
    has_documents: bool = False
    errors: List[str] = Field(default_factory=list)

from pydantic import BaseModel
from typing import List


class IntentClassification(BaseModel):
    intent: str  # must map to IntentType
    requires: List[str]  # e.g. ["LEGAL_RESEARCH", "DRAFTING"]
    
    # fine-grained signals for later routing
    needs_documents: bool = False
    needs_statute: bool = False
    needs_case_law: bool = False
    needs_web: bool = False
    needs_drafting: bool = False