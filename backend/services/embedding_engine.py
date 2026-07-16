from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Handles text embedding generation and similarity scoring using a sentence transformer model
class EmbeddingEngine:

    # Cached model instance (loaded once, shared across all calls)
    _model = None

    @classmethod
    def get_model(cls):
        # Lazily load the model only on first use, then reuse it
        if cls._model is None:
            print("Loading Sentence Transformer...")
            cls._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        return cls._model

    @classmethod
    def encode(cls, texts):
        # Get the (cached) model instance
        model = cls.get_model()
        # Convert input texts into normalized numpy embedding vectors
        return model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    @classmethod
    def similarity(
        cls,
        query_embedding,
        document_embeddings,
    ):
        # Compute cosine similarity between a single query embedding and multiple document embeddings
        return cosine_similarity(
            [query_embedding],
            document_embeddings,
        )[0]

    @classmethod
    def rank(
        cls,
        query,
        documents,
    ):
        # Encode the query string into an embedding
        query_embedding = cls.encode([query])[0]
        # Encode all candidate documents into embeddings
        document_embeddings = cls.encode(documents)
        # Score each document's similarity to the query
        scores = cls.similarity(
            query_embedding,
            document_embeddings,
        )
        return scores
