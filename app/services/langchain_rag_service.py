from typing import Dict, Any, List

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config.settings import get_settings
from storage.mongodb_client import MongoDBClient

settings = get_settings()


def get_langchain_vector_store() -> Chroma:
    """
    Connect LangChain to the same ChromaDB collection
    used by our custom RAG implementation.
    """

    embeddings = OllamaEmbeddings(
        model=settings.embedding_model,
    )

    vector_store = Chroma(
        collection_name="enterprise_documents",
        persist_directory=settings.chroma_db_path,
        embedding_function=embeddings,
    )

    return vector_store


def retrieve_with_langchain(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Retrieve relevant chunks using LangChain's Chroma wrapper.
    This does retrieval only. It does not generate an answer.
    """

    vector_store = get_langchain_vector_store()

    results = vector_store.similarity_search_with_score(
        query=question,
        k=top_k,
    )

    retrieved_results = []

    for rank, (document, score) in enumerate(results, start=1):
        metadata = document.metadata or {}

        retrieved_results.append(
            {
                "rank": rank,
                "source_file": metadata.get("source_file"),
                "document_name": metadata.get("document_name"),
                "chunk_index": metadata.get("chunk_index"),
                "score": score,
                "text_preview": document.page_content[:300],
                "full_text": document.page_content,
            }
        )

    return {
        "question": question,
        "top_k": top_k,
        "retrieved_count": len(retrieved_results),
        "results": retrieved_results,
    }


def ask_with_langchain_rag(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Full LangChain RAG flow:
    1. Retrieve chunks from ChromaDB
    2. Build context
    3. Send context + question to ChatOllama
    4. Log query in MongoDB
    5. Return answer and sources
    """

    vector_store = get_langchain_vector_store()
    mongo_client = MongoDBClient()

    results = vector_store.similarity_search_with_score(
        query=question,
        k=top_k,
    )

    if not results:
        answer = "I could not find relevant context in the document database."

        query_id = mongo_client.insert_query_log(
            {
                "question": question,
                "answer": answer,
                "sources": [],
                "top_k": top_k,
                "model": settings.chat_model,
                "framework": "langchain",
                "status": "no_relevant_context",
            }
        )

        return {
            "query_id": query_id,
            "question": question,
            "answer": answer,
            "sources": [],
            "framework": "langchain",
            "status": "no_relevant_context",
        }

    documents = [doc for doc, score in results]

    context = "\n\n---\n\n".join(
        [document.page_content for document in documents]
    )

    sources = []
    for document, score in results:
        metadata = document.metadata or {}

        sources.append(
            {
                "source_file": metadata.get("source_file"),
                "document_name": metadata.get("document_name"),
                "chunk_index": metadata.get("chunk_index"),
                "score": score,
            }
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an enterprise RAG assistant.

Answer the user's question using ONLY the provided context.
Do not use outside knowledge.
If the answer is not available in the context, say:
"I do not have enough information in the provided documents."
""",
            ),
            (
                "human",
                """
Context:
{context}

User Question:
{question}
""",
            ),
        ]
    )

    llm = ChatOllama(
        model=settings.chat_model,
        temperature=0,
    )

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    query_id = mongo_client.insert_query_log(
        {
            "question": question,
            "answer": answer,
            "sources": sources,
            "top_k": top_k,
            "model": settings.chat_model,
            "framework": "langchain",
            "status": "success",
        }
    )

    return {
        "query_id": query_id,
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": [document.page_content for document in documents],
        "model": settings.chat_model,
        "framework": "langchain",
        "status": "success",
    }