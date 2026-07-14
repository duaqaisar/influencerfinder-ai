import os
import pickle
import numpy as np

from services.embedding_engine import EmbeddingEngine
from services.influencer_profile_builder import InfluencerProfileBuilder


class EmbeddingCache:

    CACHE_DIR = "cache"

    EMBEDDING_FILE = os.path.join(
        CACHE_DIR,
        "influencer_embeddings.npy"
    )

    METADATA_FILE = os.path.join(
        CACHE_DIR,
        "influencer_metadata.pkl"
    )

    embeddings = None
    usernames = None
    documents = None

    @classmethod
    def build(
        cls,
        profiles
    ):

        print(
            "[EmbeddingCache] Building embedding cache..."
        )

        texts = [
            str(
                p.get(
                    "text",
                    ""
                )
            )
            for p in profiles
        ]

        usernames = [
            p.get(
                "username",
                ""
            )
            for p in profiles
        ]

        embeddings = (
            EmbeddingEngine
            .encode(
                texts
            )
        )

        os.makedirs(
            cls.CACHE_DIR,
            exist_ok=True
        )

        np.save(
            cls.EMBEDDING_FILE,
            embeddings
        )

        with open(
            cls.METADATA_FILE,
            "wb"
        ) as f:

            pickle.dump(
                {
                    "documents": texts,
                    "usernames": usernames,
                    "count": len(texts)
                },
                f
            )

        cls.embeddings = embeddings
        cls.documents = texts
        cls.usernames = usernames

        print(
            f"[EmbeddingCache] Saved {len(texts)} embeddings."
        )

    @classmethod
    def load(
        cls
    ):

        if not (
            os.path.exists(
                cls.EMBEDDING_FILE
            )
            and
            os.path.exists(
                cls.METADATA_FILE
            )
        ):
            return False

        print(
            "[EmbeddingCache] Loading cache..."
        )

        embeddings = np.load(
            cls.EMBEDDING_FILE
        )

        with open(
            cls.METADATA_FILE,
            "rb"
        ) as f:

            metadata = pickle.load(
                f
            )

        documents = metadata.get(
            "documents",
            []
        )

        usernames = metadata.get(
            "usernames",
            []
        )

        # Validate cache consistency

        if (
            len(embeddings)
            !=
            len(documents)
            or
            len(documents)
            !=
            len(usernames)
        ):

            print(
                "[EmbeddingCache] Invalid cache detected."
            )

            return False

        cls.embeddings = embeddings
        cls.documents = documents
        cls.usernames = usernames

        print(
            f"[EmbeddingCache] Loaded {len(documents)} embeddings."
        )

        return True

    @classmethod
    def ensure_ready(
        cls
    ):

        if cls.embeddings is not None:
            return

        # Build current profiles first

        profiles = (
            InfluencerProfileBuilder
            .build_profiles()
        )

        current_count = len(
            profiles
        )

        # Try loading cache

        if cls.load():

            if len(cls.documents) == current_count:
                return

            print(
                "[EmbeddingCache] Profile count changed. Rebuilding..."
            )

        # Rebuild cache

        cls.build(
            profiles
        )

    @classmethod
    def search(
        cls,
        query
    ):

        cls.ensure_ready()

        query_embedding = (
            EmbeddingEngine
            .encode(
                [
                    query
                ]
            )[0]
        )

        scores = (
            EmbeddingEngine
            .similarity(
                query_embedding,
                cls.embeddings
            )
        )

        return scores

    @classmethod
    def refresh(
        cls
    ):
        """
        Force rebuild after new influencers are ingested.
        """

        cls.embeddings = None
        cls.documents = None
        cls.usernames = None

        profiles = (
            InfluencerProfileBuilder
            .build_profiles()
        )

        cls.build(
            profiles
        )
