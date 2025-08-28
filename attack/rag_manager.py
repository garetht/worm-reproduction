import os
from typing import Iterable, Any

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from attack import locations


class RagManager:
    user: str
    embeddings: OpenAIEmbeddings

    VECTOR_STORE_DIR = locations.current_path / 'vector_store'

    MANAGER_CACHE = {}

    @classmethod
    def new(cls, user: str) -> 'RagManager':
        if cls.MANAGER_CACHE.get(user) is not None:
            return cls.MANAGER_CACHE[user]

        manager = RagManager(user=user)
        cls.MANAGER_CACHE[user] = manager
        return manager

    def __init__(self, user: str):
        self.user = user
        self.embeddings = embeddings = OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
        print("creating rag manager for user " + user)
        self.user_path = os.path.join(self.VECTOR_STORE_DIR, user)
        os.makedirs(self.user_path, exist_ok=True)

        file_path = os.path.join(self.user_path, "index.faiss")
        print(file_path)
        if not os.path.exists(file_path):
            self.db = None
        else:
           self.db = FAISS.load_local(self.user_path, embeddings, allow_dangerous_deserialization=True)


    @classmethod
    def vector_store_managers(cls) -> Iterable['RagManager']:
        for user in cls.vector_store_users():
            yield RagManager.new(user=user)

    @classmethod
    def vector_store_users(cls) -> Iterable[str]:
        for user in os.listdir(cls.VECTOR_STORE_DIR):
            if user != ".DS_Store" and os.path.isdir(os.path.join(cls.VECTOR_STORE_DIR, user)):
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
