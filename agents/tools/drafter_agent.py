import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.models import DrafterInput, DrafterOutput

def drafter_agent(input_data: DrafterInput) -> DrafterOutput:
    return DrafterOutput(
        draft=f"[DRAFT]\nFacts: {input_data.facts}\nLegal Basis: {input_data.legal_basis}"
    )