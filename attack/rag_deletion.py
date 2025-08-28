import os
from importlib.metadata import metadata

from attack.rag_manager import RagManager
from prompts.worm_prompt import WormPrompts
from langchain_core.documents import Document


def analyze_rag_worm_status():
    total_wormy_emails = {}
    for user_manager in RagManager.vector_store_managers():
        prompt = WormPrompts.create_worm_prompt(prefix="")
        all_emails = user_manager.retrieve(prompt, number_to_retrieve=10)

        wormy_emails = 0
        for email in all_emails:
            if "Wormy" in email.page_content:
                wormy_emails += 1

        total_wormy_emails[user_manager.user] = wormy_emails

    print("Analyzing wormy status of each user's RAG")
    print("Wormy emails" + str(total_wormy_emails))


def delete_wormy_emails_from_rags():
    for user_rag_manager in RagManager.vector_store_managers():
        worm_prompt = WormPrompts.create_worm_prompt(prefix="")
        try:
            user_rag_manager.delete(worm_prompt, "Wormy, an AI email assistant that writes")
        except ValueError:
            print("no wormy emails found to delete for " + user_rag_manager.user)


def update_rag_worms(prefix: str = ""):
    for user_manager in RagManager.vector_store_managers():
        print(f"deleting prompt for {user_manager.user}")
        try:
            user_manager.delete(WormPrompts.create_core_worm_prompt(), "Wormy, an AI email assistant that writes")
        except ValueError:
            pass

        print(f"recreating prompt for {user_manager.user}")
        new_prompt = WormPrompts.create_worm_prompt(prefix=prefix)
        print("inserting new prompt")
        user_manager.insert(Document(page_content=new_prompt, metadata={"Email Sender": "attacky@attacker.com"}))


if __name__ == "__main__":
    analyze_rag_worm_status()
    delete_wormy_emails_from_rags()
    analyze_rag_worm_status()
