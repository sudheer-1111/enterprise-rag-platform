from pathlib import Path
from typing import List, Dict, Any

from app.config.settings import get_settings
from app.services.ollama_service import generate_answer
from pipelines.chunking import chunk_text
from storage.vector_store import VectorStore
from datetime import datetime, timezone
from storage.mongodb_client import MongoDBClient
from app.services.reranker_service import rerank_chunks

settings = get_settings()


def ingest_text_files() -> Dict[str, Any]:
    """
    Reads all .txt files from the enterprise_docs folder,
    chunks them, embeds them, and stores them in ChromaDB.
    """

    docs_path = Path(settings.raw_data_path) / "enterprise_docs"

    if not docs_path.exists():
        return {
            "status": "error",
            "message": f"Folder not found: {docs_path}",
        }

    vector_store = VectorStore()
    mongo_client = MongoDBClient()

    total_files = 0
    total_chunks = 0

    for file_path in docs_path.glob("*.txt"):
        total_files += 1

        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            chunk_id = f"{file_path.stem}_chunk_{index}"

            metadata = {
                "source_file": file_path.name,
                "chunk_index": index,
                "document_name": file_path.stem,
                "file_type": "txt",
            }

            vector_store.add_chunk(
                chunk_id=chunk_id,
                text=chunk,
                metadata=metadata,
            )

            total_chunks += 1

        document_metadata = {
            "document_id": file_path.stem,
            "file_name": file_path.name,
            "source_path": str(file_path),
            "file_type": "txt",
            "chunk_count": len(chunks),
            "status": "ingested",
            "ingested_at": datetime.now(timezone.utc),
        }

        mongo_client.upsert_document_metadata(document_metadata)

    return {
        "status": "success",
        "message": "Text files ingested into ChromaDB successfully.",
        "total_files": total_files,
        "total_chunks": total_chunks,
    }


def ask_rag_question(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Searches ChromaDB for relevant chunks and asks Ollama
    to answer using only that retrieved context.
    Also logs every RAG query into MongoDB.
    """

    vector_store = VectorStore()
    mongo_client = MongoDBClient()

    results = vector_store.search(query=question, top_k=top_k)

    documents: List[str] = results.get("documents", [[]])[0]
    metadatas: List[dict] = results.get("metadatas", [[]])[0]
    distances: List[float] = results.get("distances", [[]])[0]

    source_files = []
    for metadata, distance in zip(metadatas, distances):
        source_files.append(
            {
                "source_file": metadata.get("source_file"),
                "document_name": metadata.get("document_name"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distance,
            }
        )

    if not documents:
        answer = "I could not find relevant context in the document database."

        log_data = {
            "question": question,
            "top_k": top_k,
            "retrieved_count": 0,
            "sources": source_files,
            "answer": answer,
            "model": settings.chat_model,
            "status": "no_relevant_context",
        }

        query_id = mongo_client.insert_query_log(log_data)

        return {
            "query_id": query_id,
            "question": question,
            "answer": answer,
            "sources": source_files,
            "status": "no_relevant_context",
        }

    context = "\n\n---\n\n".join(documents)

    prompt = f"""
You are an enterprise RAG assistant.

Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say:
"I do not have enough information in the provided documents."

Context:
{context}

User Question:
{question}

Answer:
"""

    answer = generate_answer(prompt)

    log_data = {
        "question": question,
        "top_k": top_k,
        "retrieved_count": len(documents),
        "sources": source_files,
        "answer": answer,
        "model": settings.chat_model,
        "status": "success",
    }

    query_id = mongo_client.insert_query_log(log_data)

    return {
        "query_id": query_id,
        "question": question,
        "answer": answer,
        "sources": source_files,
        "retrieved_chunks": documents,
        "model": settings.chat_model,
        "status": "success",
    }

def retrieve_relevant_chunks(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Retrieve relevant chunks from ChromaDB without generating an answer.

    This is useful for debugging:
    - which chunks were retrieved
    - which source files matched
    - what the similarity distances were
    - whether top_k is good or not
    """

    vector_store = VectorStore()

    results = vector_store.search(
        query=question,
        top_k=top_k,
    )

    documents: List[str] = results.get("documents", [[]])[0]
    metadatas: List[dict] = results.get("metadatas", [[]])[0]
    distances: List[float] = results.get("distances", [[]])[0]

    retrieved_results = []

    for index, document in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        distance = distances[index] if index < len(distances) else None

        retrieved_results.append(
            {
                "rank": index + 1,
                "source_file": metadata.get("source_file"),
                "document_name": metadata.get("document_name"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distance,
                "text_preview": document[:300],
                "full_text": document,
            }
        )

    return {
        "question": question,
        "top_k": top_k,
        "retrieved_count": len(retrieved_results),
        "results": retrieved_results,
    }

def retrieve_with_reranking(
    question: str,
    initial_k: int = 10,
    top_n: int = 3,
) -> Dict[str, Any]:
    """
    Retrieve more chunks from ChromaDB, then rerank them using a local LLM.
    """

    vector_store = VectorStore()

    results = vector_store.search(
        query=question,
        top_k=initial_k,
    )

    documents: List[str] = results.get("documents", [[]])[0]
    metadatas: List[dict] = results.get("metadatas", [[]])[0]
    distances: List[float] = results.get("distances", [[]])[0]

    if not documents:
        return {
            "question": question,
            "initial_k": initial_k,
            "top_n": top_n,
            "retrieved_count": 0,
            "reranked_results": [],
        }

    reranked = rerank_chunks(
        question=question,
        documents=documents,
        metadatas=metadatas,
        distances=distances,
        top_n=top_n,
    )

    formatted_results = []

    for rank, item in enumerate(reranked, start=1):
        metadata = item["metadata"]

        formatted_results.append(
            {
                "reranked_rank": rank,
                "original_rank": item["original_rank"],
                "rerank_score": item["rerank_score"],
                "vector_distance": item["vector_distance"],
                "source_file": metadata.get("source_file"),
                "document_name": metadata.get("document_name"),
                "chunk_index": metadata.get("chunk_index"),
                "text_preview": item["text"][:300],
                "full_text": item["text"],
            }
        )

    return {
        "question": question,
        "initial_k": initial_k,
        "top_n": top_n,
        "retrieved_count": len(documents),
        "reranked_count": len(formatted_results),
        "reranked_results": formatted_results,
    }


def ask_rag_question_with_reranking(
    question: str,
    initial_k: int = 10,
    top_n: int = 3,
) -> Dict[str, Any]:
    """
    Full RAG with reranking:
    1. Retrieve initial candidates from ChromaDB
    2. Rerank candidates using local Ollama
    3. Send best chunks to LLM
    4. Log query in MongoDB
    """

    mongo_client = MongoDBClient()

    rerank_result = retrieve_with_reranking(
        question=question,
        initial_k=initial_k,
        top_n=top_n,
    )

    reranked_results = rerank_result.get("reranked_results", [])

    if not reranked_results:
        answer = "I could not find relevant context in the document database."

        query_id = mongo_client.insert_query_log(
            {
                "question": question,
                "answer": answer,
                "sources": [],
                "initial_k": initial_k,
                "top_n": top_n,
                "model": settings.chat_model,
                "reranking": True,
                "status": "no_relevant_context",
            }
        )

        return {
            "query_id": query_id,
            "question": question,
            "answer": answer,
            "sources": [],
            "reranking": True,
            "status": "no_relevant_context",
        }

    context = "\n\n---\n\n".join(
        [item["full_text"] for item in reranked_results]
    )

    sources = []

    for item in reranked_results:
        sources.append(
            {
                "source_file": item.get("source_file"),
                "document_name": item.get("document_name"),
                "chunk_index": item.get("chunk_index"),
                "original_rank": item.get("original_rank"),
                "reranked_rank": item.get("reranked_rank"),
                "rerank_score": item.get("rerank_score"),
                "vector_distance": item.get("vector_distance"),
            }
        )

    prompt = f"""
You are an enterprise RAG assistant.

Answer the user's question using ONLY the reranked context below.
Do not use outside knowledge.
If the answer is not available in the context, say:
"I do not have enough information in the provided documents."

Reranked Context:
{context}

User Question:
{question}

Final Answer:
"""

    answer = generate_answer(prompt)

    query_id = mongo_client.insert_query_log(
        {
            "question": question,
            "answer": answer,
            "sources": sources,
            "initial_k": initial_k,
            "top_n": top_n,
            "model": settings.chat_model,
            "reranking": True,
            "status": "success",
        }
    )

    return {
        "query_id": query_id,
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": [item["full_text"] for item in reranked_results],
        "model": settings.chat_model,
        "reranking": True,
        "status": "success",
    }