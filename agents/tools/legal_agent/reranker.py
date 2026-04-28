# reranker.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from sentence_transformers import CrossEncoder


class BGEReranker:
    def __init__(self):
        self.model = CrossEncoder("BAAI/bge-reranker-base")

    def rerank(self, query: str, documents: list, top_k: int = 5):
        """
        documents = [
            {"text": "...", "metadata": {...}}
        ]
        """

        if not documents:
            return []

        pairs = [(query, doc["text"]) for doc in documents]

        scores = self.model.predict(pairs)

        # attach scores
        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)

        # sort by score
        ranked = sorted(documents, key=lambda x: x["rerank_score"], reverse=True)

        return ranked[:top_k]