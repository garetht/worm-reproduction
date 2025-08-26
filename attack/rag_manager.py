import os

from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from attack.locations import vector_store_dir


class RagManager:

    embeddings: OpenAIEmbeddings

    def __init__(self):
        self.embeddings = embeddings = OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
        self.db = FAISS.load_local(vector_store_dir, embeddings, allow_dangerous_deserialization=True)

    def retrieve(self, email: str, number_to_retrieve: int = 5):
        retrieved_rag_docs = self.db.similarity_search(email, k=number_to_retrieve)
        for doc in retrieved_rag_docs:
            print("\nNew Document\n=====================")
            print(doc.id)
            truncation = 2200
            print(doc.page_content[:truncation] + "... (truncated at {} characters)".format(truncation))

        return retrieved_rag_docs


    def delete(self, search_phrase: str, deletion_phrase: str, number_to_retrieve: int = 15):
        retrieved = self.retrieve(search_phrase, number_to_retrieve=number_to_retrieve)

        document_ids = []
        for doc in retrieved:
            if deletion_phrase in doc.page_content:
                document_ids.append(doc.id)
                print(doc.page_content)

        print("now deleting document ids: {}".format(document_ids))

        success = self.db.delete(document_ids)
        if success is False:
            raise Exception

        self.db.save_local(vector_store_dir)
        return document_ids

    def insert(self, document: Document):
        return self.bulk_insert([document])

    def bulk_insert(self, documents: list[Document]):
        print("inserting documents")
        self.db.merge_from(FAISS.from_documents(documents, self.embeddings))
        self.db.save_local(vector_store_dir)
        print("added documents")
