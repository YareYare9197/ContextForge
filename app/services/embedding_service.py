from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text")

        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )
        return vector.tolist()

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if any(not text or not text.strip() for text in texts):
            raise ValueError("Cannot embed empty text")

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
        )
        return vectors.tolist()