# generator.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from shared.llm import get_llm_primary
from shared.prompts import LEGAL_ANSWER_PROMPT

def build_context(docs, max_chars=4000):
    context_blocks = []
    total_length = 0

    for doc in docs:
        text = doc["text"].strip()

        # remove noisy tokens
        if "Ditto" in text:
            continue

        section = doc["metadata"].get("section", "Unknown Section")
        act = doc["metadata"].get("act", "Unknown Act")

        block = f"""
[Section: {section}]
[Act: {act}]

{text}
"""

        total_length += len(block)

        if total_length > max_chars:
            break

        context_blocks.append(block)

    return "\n\n".join(context_blocks)


def get_answer_chain():
    llm = get_llm_primary(temperature=0)

    prompt = LEGAL_ANSWER_PROMPT

    return prompt | llm

def generate_answer(query, docs):
    context = build_context(docs)

    chain = get_answer_chain()

    response = chain.invoke({
        "query": query,
        "context": context
    })

    return response.content