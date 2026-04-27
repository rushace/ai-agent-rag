import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.models import LegalResearchInput, LegalResearchOutput
def legal_web_researcher_agent(input_data: LegalResearchInput) -> LegalResearchOutput:
    return LegalResearchOutput(
        analysis=f"[LEGAL] Analysis for: {input_data.query}",
        acts=["IPC Section 420"],
        cases=["ABC vs State"],
        web=[]
    )