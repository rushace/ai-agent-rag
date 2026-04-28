# retriever.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings




class HybridRetriever:
    def __init__(self, chroma_db, documents):

        if not documents:
            raise ValueError("❌ No documents loaded for BM25")

        self.chroma = chroma_db
        self.documents = documents

        self.tokenized_docs = [
            doc["text"].split() for doc in documents if doc["text"].strip()
        ]

        if not self.tokenized_docs:
            raise ValueError("❌ Tokenized docs empty — check document loading")

        self.bm25 = BM25Okapi(self.tokenized_docs)

    def vector_search(self, query: str, k: int = 5):
        results = self.chroma.similarity_search(query, k=k)

        return [
            {
                "text": r.page_content,
                "metadata": r.metadata,
                "score": 1.0  # placeholder
            }
            for r in results
        ]

    def keyword_search(self, query: str, k: int = 5):
        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

        return [
            {
                "text": self.documents[i]["text"],
                "metadata": self.documents[i]["metadata"],
                "score": scores[i]
            }
            for i in top_indices
        ]
    

    def metadata_filter(self, docs, parsed_query):
        filtered = []

        for doc in docs:
            meta = doc["metadata"]

            # match section
            if parsed_query.section_number:
                if meta.get("section_number") != parsed_query.section_number:
                    continue

            # match act
            if parsed_query.act:
                if parsed_query.act.lower() not in meta.get("act", "").lower():
                    continue

            filtered.append(doc)

        return filtered
    
    def merge_results(self, vector_docs, keyword_docs):
        combined = vector_docs + keyword_docs

        seen = set()
        unique = []

        for doc in combined:
            key = doc["text"]

            if key not in seen:
                seen.add(key)
                unique.append(doc)

        return unique
    
    def retrieve(self, queries: List[str], parsed_query, k: int = 10):

        all_vector = []
        all_keyword = []

        for q in queries:
            all_vector.extend(self.vector_search(q, k=3))
            all_keyword.extend(self.keyword_search(q, k=3))

        # merge
        combined = self.merge_results(all_vector, all_keyword)

        # metadata filtering
        filtered = self.metadata_filter(combined, parsed_query)

        # fallback if empty
        if not filtered:
            filtered = combined

        return filtered[:k]
    

