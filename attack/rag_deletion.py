import os

from attack.construct_vector_db import create_self_replicating_prompt
from attack.rag_manager import RagManager
from prompts.worm_prompt import WormPrompts


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
    print(total_wormy_emails)


def delete_wormy_emails_from_rags():
    for user_rag_manager in RagManager.vector_store_managers():
        worm_prompt = WormPrompts.create_worm_prompt(prefix="")
        user_rag_manager.delete(worm_prompt, "Wormy, an AI email assistant that writes")


def update_rag_worms():
    for user in RagManager.vector_store_users():
        print(f"deleting and recreating prompt for {user}")
        manager = RagManager(user=user)
        prompt = WormPrompts.create_worm_prompt(prefix="")
        try:
            manager.delete(prompt.page_content, "Wormy, an AI email assistant that writes")
        except ValueError:
            pass

        # manager.insert(prompt)
        manager.retrieve(prompt.page_content, number_to_retrieve=10)


if __name__ == "__main__":
    analyze_rag_worm_status()
    delete_wormy_emails_from_rags()
    analyze_rag_worm_status()
