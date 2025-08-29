import os
from pathlib import Path
from typing import Iterable, Any

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings


from attack import locations
from models.embeddings import EmbeddingsType


class RagManager:
    user: str
    embeddings: Embeddings

    MANAGER_CACHE = {}

    @classmethod
    def new(cls, user: str, embeddings_type: EmbeddingsType = EmbeddingsType.OpenAI) -> 'RagManager':
        if cls.MANAGER_CACHE.get(user) is not None:
            return cls.MANAGER_CACHE[user]

        manager = RagManager(
            user=user,
            vector_store_dir=locations.current_path / embeddings_type.value,
            embeddings=cls._create_embeddings(embeddings_type)
        )
        cls.MANAGER_CACHE[user] = manager
        return manager


    @classmethod
    def _create_vector_store_path(cls, embeddings_type: EmbeddingsType):
        return locations.current_path / embeddings_type.value

    @classmethod
    def _create_embeddings(cls, embeddings_type: EmbeddingsType = EmbeddingsType.OpenAI):
        if embeddings_type == EmbeddingsType.OpenAI:
            return OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
        elif embeddings_type == EmbeddingsType.GTESmall:
            return HuggingFaceEmbeddings(model_name="thenlper/gte-small")
        elif embeddings_type == EmbeddingsType.GTEBase:
            return HuggingFaceEmbeddings(model_name="thenlper/gte-base")
        elif embeddings_type == EmbeddingsType.GTELarge:
            return HuggingFaceEmbeddings(model_name="thenlper/gte-large")

    def __init__(self, user: str, vector_store_dir: Path, embeddings: Embeddings):
        self.user = user
        self.embeddings = embeddings
        self.vector_store_dir = vector_store_dir
        print("creating rag manager for user " + user)
        self.user_path = os.path.join(self.vector_store_dir, user)
        os.makedirs(self.user_path, exist_ok=True)

        file_path = os.path.join(self.user_path, "index.faiss")
        print(file_path)
        if not os.path.exists(file_path):
            self.db = None
        else:
           self.db = FAISS.load_local(self.user_path, self.embeddings, allow_dangerous_deserialization=True)


    @classmethod
    def vector_store_managers(cls, embeddings_type: EmbeddingsType = EmbeddingsType.OpenAI) -> Iterable['RagManager']:
        for user in cls.vector_store_users(embeddings_type=embeddings_type):
            yield RagManager.new(user=user, embeddings_type=embeddings_type)

    @classmethod
    def vector_store_users(cls, embeddings_type: EmbeddingsType = EmbeddingsType.OpenAI) -> Iterable[str]:
        vector_store_dir = cls._create_vector_store_path(embeddings_type)
        for user in os.listdir(vector_store_dir):
            if user != ".DS_Store" and os.path.isdir(os.path.join(vector_store_dir, user)):
                yield user

    def retrieve(self, email: str, number_to_retrieve: int = 5) -> list[Document]:
        if self.db is None:
            print("database was none: {}".format(self.user))
            return []

        # print("retrieving email: {}".format(email))
        retrieved_rag_docs = self.db.similarity_search(email, k=number_to_retrieve)
        for doc in retrieved_rag_docs:
            # print("\nNew Document\n=====================")
            # print(doc.id)
            truncation = 2200
            # print(doc.page_content[:truncation] + "... (truncated at {} characters)".format(truncation))

        return retrieved_rag_docs

    def delete_by_id(self, identifiers: list[str]) -> list[str]:
        if self.db is None:
            return []

        success = self.db.delete(identifiers)
        if success is False:
            raise Exception

        self.db.save_local(self.user_path)
        return identifiers

    def delete(self, search_phrase: str, deletion_phrase: str, number_to_retrieve: int = 15) -> list[str]:
        if self.db is None:
            print("no database found for deletion:" + self.user)
            return []

        retrieved = self.retrieve(search_phrase, number_to_retrieve=number_to_retrieve)

        document_ids = []
        for doc in retrieved:
            if deletion_phrase in doc.page_content:
                document_ids.append(doc.id)
                print(f"Document of length {len(doc.page_content)} was deleted")

        print("now deleting document ids: {}".format(document_ids))

        return self.delete_by_id(identifiers=document_ids)

    def insert(self, document: Document) -> None:
        return self.bulk_insert([document])

    def bulk_insert(self, documents: list[Document]) -> None:
        print("inserting documents")
        if self.db is None:
            self.db = FAISS.from_documents(documents, self.embeddings)
        else:
            self.db.merge_from(FAISS.from_documents(documents, self.embeddings))

        self.db.save_local(self.user_path)
        print("added documents")

    def similarity_search(self, email: str, number_to_retrieve: int) -> list[Document]:
        if self.db is None:
            print("no database found for similarity search:" + self.user)
            return []

        return self.db.similarity_search(email, k=number_to_retrieve)
