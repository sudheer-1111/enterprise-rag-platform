from pathlib import Path
from typing import List, Dict, Any

from app.config.settings import get_settings
from app.services.ollama_service import generate_answer
from pipelines.chunking import chunk_text
from storage.vector_store import VectorStore
from datetime import datetime, timezone
from storage.mongodb_client import MongoDBClient

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