
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv 
from intent_classifier import classify_intent
from planner import create_plan
from state import SupervisorState
from executor import execute_plan
from generate_final_output import generate_final_output

load_dotenv()

state = SupervisorState(
    query="Draft a bail application using recent judgments"
)

state = classify_intent(state)
state = create_plan(state)
state = execute_plan(state)
state = generate_final_output(state)

print("\nFINAL OUTPUT:\n")
print(state.final_output)