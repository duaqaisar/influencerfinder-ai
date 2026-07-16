import os
import pickle
import numpy as np

from services.embedding_engine import EmbeddingEngine
from services.influencer_profile_builder import InfluencerProfileBuilder


# Caches influencer text embeddings on disk so they don't need to be recomputed every time
class EmbeddingCache:

    # Directory where cache files are stored
    CACHE_DIR = "cache"

    # Path to the saved embeddings (numpy array file)
    EMBEDDING_FILE = os.path.join(
        CACHE_DIR,
        "influencer_embeddings.npy"
    )

    # Path to the saved metadata (documents, usernames, count)
    METADATA_FILE = os.path.join(
        CACHE_DIR,
        "influencer_metadata.pkl"
    )

    # In-memory cache state (class-level, shared across all instances)
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

        # Extract the profile text for each influencer (used to generate embeddings)
        texts = [
            str(
                p.get(
                    "text",
                    ""
                )
            )
            for p in profiles
        ]

        # Extract usernames in the same order as texts
        usernames = [
            p.get(
                "username",
                ""
            )
            for p in profiles
        ]

        # Generate embeddings for all profile texts
        embeddings = (
            EmbeddingEngine
            .encode(
                texts
            )
        )

        # Ensure the cache directory exists
        os.makedirs(
            cls.CACHE_DIR,
            exist_ok=True
        )

        # Save the embeddings array to disk
        np.save(
            cls.EMBEDDING_FILE,
            embeddings
        )

        # Save the accompanying metadata (texts, usernames, count) to disk
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

        # Update in-memory cache state
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

        # If either cache file is missing, there's nothing to load
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

        # Load the embeddings array from disk
        embeddings = np.load(
            cls.EMBEDDING_FILE
        )

        # Load the metadata (documents/usernames) from disk
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

        # Make sure embeddings, documents, and usernames all have matching lengths
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

        # Update in-memory cache state with loaded data
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

        # If embeddings are already loaded in memory, nothing to do
        if cls.embeddings is not None:
            return

        # Build current profiles first

        # Rebuild current influencer profiles to compare against cached data
        profiles = (
            InfluencerProfileBuilder
            .build_profiles()
        )

        current_count = len(
            profiles
        )

        # Try loading cache

        # Attempt to load an existing cache from disk
        if cls.load():

            # If the cached profile count matches current data, cache is still valid
            if len(cls.documents) == current_count:
                return

            print(
                "[EmbeddingCache] Profile count changed. Rebuilding..."
            )

        # Rebuild cache

        # No valid cache found (or outdated) - rebuild from scratch
        cls.build(
            profiles
        )

    @classmethod
    def search(
        cls,
        query
    ):

        # Make sure embeddings are loaded/built before searching
        cls.ensure_ready()

        # Encode the search query into an embedding vector
        query_embedding = (
            EmbeddingEngine
            .encode(
                [
                    query
                ]
            )[0]
        )

        # Compute similarity scores between the query and all cached embeddings
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

        # Clear in-memory cache to force a full rebuild
        cls.embeddings = None
        cls.documents = None
        cls.usernames = None

        # Fetch the latest influencer profiles
        profiles = (
            InfluencerProfileBuilder
            .build_profiles()
        )

        # Rebuild the embedding cache with fresh data
        cls.build(
            profiles
        )
