import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from shared.prompts import intent_prompt
from shared.llm import get_llm
from state import SupervisorState,IntentClassification

def classify_intent(state: SupervisorState) -> SupervisorState:
    llm = get_llm()
    intent_chain = intent_prompt | llm.with_structured_output(IntentClassification)
    result = intent_chain.invoke({"query": state.query})
    
    state.intent = result.intent
    
    # store extra signals inside state (optional but useful)
    state.intermediate_results.append({
        "step": "intent_classification",
        "result": result.model_dump()
    })
    
    return state