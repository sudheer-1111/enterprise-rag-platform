import ollama
from app.config.settings import get_settings

settings = get_settings()


def generate_answer(prompt: str) -> str:
    response = ollama.chat(
        model=settings.chat_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise RAG assistant. "
                    "Answer clearly, professionally, and practically."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response["message"]["content"]


def generate_embedding(text: str) -> list[float]:
    response = ollama.embeddings(
        model=settings.embedding_model,
        prompt=text,
    )

    return response["embedding"]