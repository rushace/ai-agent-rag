from state import SupervisorState

def generate_final_output(state: SupervisorState) -> SupervisorState:
    last_output = state.intermediate_results[-1]["output"]

    if hasattr(last_output, "draft"):
        state.final_output = last_output.draft
    elif hasattr(last_output, "analysis"):
        state.final_output = last_output.analysis
    elif hasattr(last_output, "answer"):
        state.final_output = last_output.answer
    else:
        state.final_output = str(last_output)

    return state