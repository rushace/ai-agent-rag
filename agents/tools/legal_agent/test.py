# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from query_processor import analyze_query
# from query_expander import expand_queries
# from retriver import HybridRetriever
# from rich import print
# from reranker import BGEReranker
# from generator import generate_answer


# def load_vector_db(persist_directory="content/data/chroma_db"):
#     """Load the existing vector database"""
#     print(f"📂 Loading vector database from: {persist_directory}")

#     embedding_model = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     vectorstore = Chroma(
#         persist_directory=persist_directory,
#         embedding_function=embedding_model,
#         collection_name="legal_bare_acts"
#     )

#     print(f"✅ Vector database loaded successfully! Total documents: {vectorstore._collection.count()}")
#     return vectorstore


# def load_documents_from_chroma(chroma_db, batch_size=1000):
#     total_docs = chroma_db._collection.count()
#     documents = []

#     print(f"📦 Total docs: {total_docs}")

#     for i in range(0, total_docs, batch_size):

#         batch = chroma_db.get(
#             limit=batch_size,
#             offset=i
#         )

#         for j in range(len(batch["documents"])):
#             documents.append({
#                 "text": batch["documents"][j],
#                 "metadata": batch["metadatas"][j]
#             })

#     return documents




# db = load_vector_db("data/vector_db/bare_acts_db")
# docs = load_documents_from_chroma(db)


# retriever = HybridRetriever(db, docs)
# # -----------------------------
# # TEST QUERY
# # -----------------------------
# reranker = BGEReranker()

# query = "Explain section Muslim marriage act " 

# print("\nUSER QUERY:", query)


# # Step 1: Parse
# parsed = analyze_query(query)
# print("\nPARSED QUERY:", parsed.model_dump())


# # Step 2: Expand
# queries = expand_queries(parsed)
# print("\nEXPANDED QUERIES:")
# for q in queries:
#     print("-", q)


# # Step 3: Retrieve
# results = retriever.retrieve(queries, parsed)
# print("Retrival Completed....")


# reranked = reranker.rerank(
#     query=parsed.clean_query,
#     documents=results,
#     top_k=5
# )

# print("Reranking Completed...")
# answer = generate_answer(query, reranked)

# print("\nFINAL ANSWER:\n")
# print(answer)