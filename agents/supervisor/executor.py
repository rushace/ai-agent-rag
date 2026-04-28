import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from state import *
from utils import extract_document_type, extract_facts
from agents.tools.document_agent import document_intelligence_agent
from agents.tools.legal_agent.pipeline import legal_rag_pipeline
from agents.tools.drafter_agent import drafter_agent
from shared.models import LegalResearchOutput, DocumentAgentOutput, DrafterOutput, LegalResearchInput, DocumentAgentInput, DrafterInput

def execute_plan(state: SupervisorState) -> SupervisorState:

    for step in state.plan:

        # ---------------------------
        # DOCUMENT AGENT
        # ---------------------------
        if step.agent == "document_intelligence_agent":

            input_data = DocumentAgentInput(
                query=state.query,
                task="qa"
            )

            result = document_intelligence_agent(input_data)

        # ---------------------------
        # LEGAL RESEARCH AGENT
        # ---------------------------
        elif step.agent == "legal_web_researcher_agent":

            intent_data = state.intermediate_results[0]["result"]

            input_data = LegalResearchInput(
                query=state.query,
                needs_statute=intent_data.get("needs_statute", False),
                needs_case_law=intent_data.get("needs_case_law", False),
                needs_web=intent_data.get("needs_web", False)
            )

            result = legal_rag_pipeline(state.query)

        # ---------------------------
        # DRAFTER AGENT
        # ---------------------------
        elif step.agent == "drafter_agent":

            prev_output = state.intermediate_results[-1]["output"]

            if isinstance(prev_output, LegalResearchOutput):
                legal_basis = f"""
        Legal Analysis:
        {prev_output.analysis}

        Acts:
        {", ".join(prev_output.acts)}

        Cases:
        {", ".join(prev_output.cases)}
        """
            else:
                legal_basis = str(prev_output)

            document_type = extract_document_type(state.query)
            facts = extract_facts(state.query)

            input_data = DrafterInput(
                document_type=document_type,
                facts=facts,
                legal_basis=legal_basis
            )

            result = drafter_agent(input_data)
        else:
            state.errors.append(f"Unknown agent: {step.agent}")
            continue

        # ---------------------------
        # STORE RESULT
        # ---------------------------
        state.intermediate_results.append({
            "step": step.agent,
            "output": result["answer"]
        })

    return state