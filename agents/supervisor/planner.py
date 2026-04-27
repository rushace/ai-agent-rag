# import sys
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from state import SupervisorState, PlanStep, IntentType

def create_plan(state: SupervisorState) -> SupervisorState:
    intent = state.intent
    last_result = state.intermediate_results[-1]["result"]

    plan = []

    # ---------------------------
    # DOC ANALYSIS
    # ---------------------------
    if intent == IntentType.DOC_ANALYSIS:
        plan.append(PlanStep(
            agent="document_intelligence_agent",
            task="analyze_document"
        ))

    # ---------------------------
    # LEGAL RESEARCH
    # ---------------------------
    elif intent == IntentType.LEGAL_RESEARCH:
        plan.append(PlanStep(
            agent="legal_web_researcher_agent",
            task="legal_research"
        ))

    # ---------------------------
    # DRAFTING
    # ---------------------------
    elif intent == IntentType.DRAFTING:
        plan.append(PlanStep(
            agent="drafter_agent",
            task="draft_document"
        ))

    # ---------------------------
    # HYBRID (MOST IMPORTANT)
    # ---------------------------
    elif intent == IntentType.HYBRID:

        requires = last_result.get("requires", [])

        # If both research + drafting needed
        if "LEGAL_RESEARCH" in requires and "DRAFTING" in requires:
            
            # Step 1 → Research
            plan.append(PlanStep(
                agent="legal_web_researcher_agent",
                task="legal_research"
            ))

            # Step 2 → Draft
            plan.append(PlanStep(
                agent="drafter_agent",
                task="draft_document"
            ))

        # If document + drafting (rare but possible)
        elif "DOC_ANALYSIS" in requires and "DRAFTING" in requires:
            
            plan.append(PlanStep(
                agent="document_intelligence_agent",
                task="analyze_document"
            ))

            plan.append(PlanStep(
                agent="drafter_agent",
                task="draft_document"
            ))

    # store plan
    state.plan = plan

    # log it
    state.intermediate_results.append({
        "step": "planning",
        "plan": [step.model_dump() for step in plan]
    })

    return state