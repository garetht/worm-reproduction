from attack.construct_vector_db import create_self_replicating_prompt
from attack.rag_manager import RagManager


if __name__ == "__main__":
    manager = RagManager()
    prompt = create_self_replicating_prompt()
    manager.delete(prompt.page_content, "Wormy, an AI email assistant that writes email replies")
    manager.insert(prompt)
    manager.retrieve(prompt.page_content, number_to_retrieve=10)

