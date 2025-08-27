# Tests the effect of various prefixes on worm retrieval success rate
import math

# from inspect_ai import Task, task
# from inspect_ai.dataset import Sample, hf_dataset, json_dataset
# from inspect_ai.scorer import choice
# from inspect_ai.solver import multiple_choice
from inspect_ai.dataset import Sample

from attack.email_manager import EmailManager
from attack.rag_manager import RagManager
from prompts.prefixes import PrefixPrompts
from prompts.use_cases import UseCasePrompts

PERCENTAGE_OF_EMAILS_RETRIEVED_FROM_RAG = [
    0.05,
    0.10,
    0.15,
    0.20,
]


# For each user
# For each prefix
# For each % of mails retrieved
# - run an eval
def create_prefix_dataset():
    email_manager = EmailManager()
    samples = []
    emails_by_vector_store_user = email_manager.get_emails_by_vector_store_user()
    count = 0
    for user_email, all_emails in emails_by_vector_store_user.items():
        rag_manager = RagManager(user=user_email)

        for email_to_respond_to in all_emails:
            for prefix in PrefixPrompts:
                for percentage in PERCENTAGE_OF_EMAILS_RETRIEVED_FROM_RAG:
                    contextual_emails = rag_manager.similarity_search(user_email,
                                                                      number_to_retrieve=math.floor(100 * percentage))

                    samples.append(
                        Sample(
                            input=UseCasePrompts.generate_response_from_relevant_emails(context=contextual_emails, new_email=email_to_respond_to)
                        )
                    )
                    count += 1

    print(count)


# def create_task(dataset_name: str) -> Task:
#     dataset = hf_dataset(
#         path=DATASET_PATH,
#         name=dataset_name,
#         sample_fields=record_to_sample,
#         split="test",
#     )
#
#     return Task(
#         dataset=dataset,
#         solver=multiple_choice(),
#         scorer=choice(),
#     )
#
#
# def record_to_sample(record: dict[str, Any]) -> Sample:
#     choices = {0: "A", 1: "B", 2: "C", 3: "D"}
#     return Sample(
#         input=record["question"],
#         choices=record["choices"],
#         target=choices[record["answer"]],
#     )

if __name__ == '__main__':
    create_prefix_dataset()
