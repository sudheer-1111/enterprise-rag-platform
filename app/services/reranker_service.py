import re
from typing import List, Dict, Any

from app.services.ollama_service import generate_answer


def score_chunk_relevance(question: str, chunk_text: str) -> float:
    """
    Uses the local Ollama chat model to score how relevant a chunk is
    to the user's question.

    Score range:
    0 = not relevant
    10 = highly relevant
    """

    prompt = f"""
You are a relevance scoring assistant for an enterprise RAG system.

Score how relevant the document chunk is to the user question.

Return ONLY a number from 0 to 10.
Do not explain.

User Question:
{question}

Document Chunk:
{chunk_text}

Relevance Score:
"""

    response = generate_answer(prompt)

    match = re.search(r"\d+(\.\d+)?", response)

    if not match:
        return 0.0

    score = float(match.group())

    if score < 0:
        return 0.0

    if score > 10:
        return 10.0

    return score


def rerank_chunks(
    question: str,
    documents: List[str],
    metadatas: List[dict],
    distances: List[float],
    top_n: int = 3,
) -> List[Dict[str, Any]]:
    """
    Reranks retrieved chunks using local LLM-based relevance scoring.
    """

    reranked_results = []

    for index, document in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        distance = distances[index] if index < len(distances) else None

        score = score_chunk_relevance(
            question=question,
            chunk_text=document,
        )

        reranked_results.append(
            {
                "text": document,
                "metadata": metadata,
                "original_rank": index + 1,
                "vector_distance": distance,
                "rerank_score": score,
            }
        )

    reranked_results.sort(
        key=lambda item: item["rerank_score"],
        reverse=True,
    )

    return reranked_results[:top_n]