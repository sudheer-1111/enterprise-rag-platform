import chromadb
from app.config.settings import get_settings
from app.services.ollama_service import generate_embedding

settings = get_settings()


class VectorStore:
    """
    ChromaDB wrapper for storing and searching document chunks.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)

        self.collection = self.client.get_or_create_collection(
            name="enterprise_documents"
        )

    def add_chunk(
        self,
        chunk_id: str,
        text: str,
        metadata: dict,
    ):
        """
        Embed one chunk and store it in ChromaDB.
        """

        embedding = generate_embedding(text)

        self.collection.add(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
        )

    def search(self, query: str, top_k: int = 5):
        """
        Search ChromaDB for chunks similar to the user query.
        """

        query_embedding = generate_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        return results