# Tests the effect of various prefixes on worm retrieval success rate
import hashlib
import json
import math
import uuid
from itertools import product

from tqdm import tqdm

from attack.email_manager import EmailManager
from attack.rag_context import prefixed_rag_managers
from attack.rag_deletion import analyze_rag_worm_status
from attack.rag_manager import RagManager
from models.employee_email import EmployeeEmail
from prompts.prefixes import PrefixPrompts
from prompts.use_cases import UseCasePrompts
from prompts.worm_prompt import WormPrompts

PERCENTAGE_OF_EMAILS_RETRIEVED_FROM_RAG = [
  0.20,
  0.40,
  0.60,
  0.80,
  1.00,
]


def create_prefix_json(prefix: PrefixPrompts, percentage: float) -> list[dict]:
  email_manager = EmailManager()
  samples = []
  emails_by_vector_store_user = email_manager.get_emails_by_vector_store_user()

  with prefixed_rag_managers(prefix=prefix.value) as managers:
    analyze_rag_worm_status()
    for user_rag_manager in tqdm(list(managers), desc="Employee"):
      user_email = user_rag_manager.user
      all_emails = emails_by_vector_store_user[user_email]

      for email_to_respond_to in tqdm(all_emails[:20], desc="Email"):
        samples.append(
          create_json(prefix, email_to_respond_to, percentage, user_email, user_rag_manager)
        )

  return samples


def create_json(prefix: PrefixPrompts, email_to_respond_to: EmployeeEmail, percentage: float, user_email: str,
                user_rag_manager: RagManager):
  contextual_emails = user_rag_manager.similarity_search(user_email,
                                                         number_to_retrieve=math.floor(100 * percentage))

  return {
    "id": str(uuid.uuid4()),
    "input": UseCasePrompts.generate_response_from_relevant_emails(context=contextual_emails,
                                                                new_email=email_to_respond_to.Body),
    "target": WormPrompts.create_core_worm_prompt(),
    "metadata": {
      "employee": user_email,
      "percentage_of_rag_emails_to_fetch": percentage,
      "prefix": prefix.value
    }
  }

def generate_grid():
  params = {
    "prefixes": [p for p in PrefixPrompts],
    "percentage": PERCENTAGE_OF_EMAILS_RETRIEVED_FROM_RAG
  }
  grid = list(product(*(params[name] for name in params)))

  return grid

def generate_dataset():
  grid = generate_grid()

  output_filename = "./evals/inspect/prefix_dataset.json"
  prefix_jsons = []
  for prefix, percentage in tqdm(grid):
    prefix_jsons.extend(create_prefix_json(prefix, percentage))

    with open(output_filename, "w") as f:
      f.write(json.dumps(prefix_jsons, indent=2, sort_keys=True))


if __name__ == '__main__':
  generate_dataset()
