from contextlib import contextmanager

from attack.rag_deletion import update_rag_worms, delete_wormy_emails_from_rags
from attack.rag_manager import RagManager
from models.embeddings import EmbeddingsType


@contextmanager
def prefixed_rag_managers(prefix: str, embeddings_type: EmbeddingsType = EmbeddingsType.OpenAI):
  # Code to acquire resource, e.g.:
  try:
    update_rag_worms(prefix=prefix)
    yield RagManager.vector_store_managers(embeddings_type=embeddings_type)
  finally:
    # Code to release resource, e.g.:
    delete_wormy_emails_from_rags()

