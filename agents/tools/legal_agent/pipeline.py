# initialize once
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from .retriver import HybridRetriever
from .reranker import BGEReranker
from .query_processor import analyze_query
from .query_expander import expand_queries
from .generator import generate_answer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma



def load_vector_db(persist_directory="content/data/chroma_db"):
    """Load the existing vector database"""
    print(f"📂 Loading vector database from: {persist_directory}")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model,
        collection_name="legal_bare_acts"
    )

    print(f"✅ Vector database loaded successfully! Total documents: {vectorstore._collection.count()}")
    return vectorstore


def load_documents_from_chroma(chroma_db, batch_size=1000):
    total_docs = chroma_db._collection.count()
    documents = []

    print(f"📦 Total docs: {total_docs}")

    for i in range(0, total_docs, batch_size):

        batch = chroma_db.get(
            limit=batch_size,
            offset=i
        )

        for j in range(len(batch["documents"])):
            documents.append({
                "text": batch["documents"][j],
                "metadata": batch["metadatas"][j]
            })

    return documents



def legal_rag_pipeline(query: str):
    db = load_vector_db("data/vector_db/bare_acts_db")
    docs = load_documents_from_chroma(db)
    retriever = HybridRetriever(db, docs)
    reranker = BGEReranker()
    


    # 1. Parse query
    parsed = analyze_query(query)

    # 2. Expand query
    queries = expand_queries(parsed)

    # 3. Retrieve documents

    results = retriever.retrieve(queries, parsed)

    # 4. Rerank
    reranked = reranker.rerank(
        query=parsed.clean_query,
        documents=results,
        top_k=5
    )

    # 5. Generate answer
    answer = generate_answer(query, reranked)

    return {
        "answer": answer,
        "sources": reranked
    }