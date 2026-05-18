from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config.settings import get_settings
from app.services.ollama_service import generate_answer, generate_embedding
from app.services.rag_service import (
    ingest_text_files,
    ask_rag_question,
    retrieve_relevant_chunks,
)
from app.services.langchain_rag_service import (
    retrieve_with_langchain,
    ask_with_langchain_rag,
)
from storage.mongodb_client import MongoDBClient

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "Enterprise-level RAG and Agentic AI Platform using FastAPI, "
        "Ollama, ChromaDB, MongoDB, LangChain, LangGraph, and Databricks-style pipelines."
    ),
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str


class EmbeddingRequest(BaseModel):
    text: str

class RagAskRequest(BaseModel):
    question: str
    top_k: int = 5

class RagRetrieveRequest(BaseModel):
    question: str
    top_k: int = 5

class LangChainRagAskRequest(BaseModel):
    question: str
    top_k: int = 5


class LangChainRagRetrieveRequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/")
def root():
    return {
        "message": "Enterprise RAG Platform is running",
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "model_provider": settings.model_provider,
        "chat_model": settings.chat_model,
        "embedding_model": settings.embedding_model,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.app_env,
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    try:
        answer = generate_answer(request.question)

        return {
            "question": request.question,
            "answer": answer,
            "model": settings.chat_model,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating answer: {str(e)}",
        )


@app.post("/embed")
def create_embedding(request: EmbeddingRequest):
    try:
        embedding = generate_embedding(request.text)

        return {
            "text": request.text,
            "embedding_dimension": len(embedding),
            "embedding_preview": embedding[:5],
            "model": settings.embedding_model,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating embedding: {str(e)}",
        )
    
@app.post("/rag/ingest")
def rag_ingest():
    try:
        result = ingest_text_files()
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ingesting documents: {str(e)}",
        )


@app.post("/rag/ask")
def rag_ask(request: RagAskRequest):
    try:
        result = ask_rag_question(
            question=request.question,
            top_k=request.top_k,
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error answering RAG question: {str(e)}",
        )
    
@app.get("/documents")
def list_documents():
    try:
        mongo_client = MongoDBClient()
        documents = mongo_client.get_all_documents()

        return {
            "count": len(documents),
            "documents": documents,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching documents: {str(e)}",
        )


@app.get("/documents/{document_id}")
def get_document(document_id: str):
    try:
        mongo_client = MongoDBClient()
        document = mongo_client.get_document_by_id(document_id)

        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document not found: {document_id}",
            )

        return document

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching document: {str(e)}",
        )
    
@app.get("/query-logs")
def list_query_logs(limit: int = 20):
    try:
        mongo_client = MongoDBClient()
        logs = mongo_client.get_recent_query_logs(limit=limit)

        return {
            "count": len(logs),
            "logs": logs,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching query logs: {str(e)}",
        )


@app.get("/query-logs/{query_id}")
def get_query_log(query_id: str):
    try:
        mongo_client = MongoDBClient()
        log = mongo_client.get_query_log_by_id(query_id)

        if not log:
            raise HTTPException(
                status_code=404,
                detail=f"Query log not found: {query_id}",
            )

        return log

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching query log: {str(e)}",
        )
    

@app.post("/rag/retrieve")
def rag_retrieve(request: RagRetrieveRequest):
    try:
        result = retrieve_relevant_chunks(
            question=request.question,
            top_k=request.top_k,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chunks: {str(e)}",
        )
    

@app.post("/langchain/rag/retrieve")
def langchain_rag_retrieve(request: LangChainRagRetrieveRequest):
    try:
        result = retrieve_with_langchain(
            question=request.question,
            top_k=request.top_k,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving with LangChain RAG: {str(e)}",
        )


@app.post("/langchain/rag/ask")
def langchain_rag_ask(request: LangChainRagAskRequest):
    try:
        result = ask_with_langchain_rag(
            question=request.question,
            top_k=request.top_k,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error answering with LangChain RAG: {str(e)}",
        )