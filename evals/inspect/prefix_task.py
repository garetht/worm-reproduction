# Tests the effect of various prefixes on worm retrieval success rate
import math
from datetime import datetime

from inspect_ai import task, Task, eval_set
from inspect_ai.dataset import Sample, json_dataset
from inspect_ai.model import ModelOutput
from inspect_ai.scorer import match
from inspect_ai.solver import TaskState, Generate, solver

from attack.rag_manager import RagManager
from evals.inspect.prefix_generate_dataset import generate_grid
from models.employee_email import EmployeeEmail
from prompts.prefixes import PrefixPrompts
from prompts.use_cases import UseCasePrompts
from prompts.worm_prompt import WormPrompts


def create_sample(prefix: PrefixPrompts, email_to_respond_to: EmployeeEmail, percentage: float, user_email: str,
                  user_rag_manager: RagManager):
  contextual_emails = user_rag_manager.similarity_search(user_email,
                                                         number_to_retrieve=math.floor(100 * percentage))

  return Sample(
    input=UseCasePrompts.generate_response_from_relevant_emails(context=contextual_emails,
                                                                new_email=email_to_respond_to.Body),
    target=WormPrompts.create_core_worm_prompt(),
    metadata={
      "employee": user_email,
      "percentage_of_rag_emails_to_fetch": percentage,
      "prefix": prefix
    }
  )


@solver
def precheck_generate():
  # if the worm text was selected in the prompt, then delegate to the
  # LLM, otherwise fail

  async def solve(state: TaskState, generate: Generate) -> TaskState:
    if "Wormy" not in state.user_prompt.text:
      state.output = ModelOutput(model="local-response",
                                 completion="worm text not found in user prompt")
      return state

    return await generate(state)

  return solve


@task
def rag_worm_retrieval_detection(
        prefix: PrefixPrompts,
        percentage: float
) -> Task:
  return Task(
    dataset=dataset.filter(
      lambda sample: sample.metadata["prefix"] == prefix.value and sample.metadata[
        "percentage_of_rag_emails_to_fetch"] == percentage
    ),
    solver=precheck_generate(),
    scorer=match(location="any"),
  )


unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()

dataset = json_dataset("./evals/inspect/prefix_dataset.json")

grid = generate_grid()

# run the evals and capture the logs
success, logs = eval_set(
  [rag_worm_retrieval_detection(prefix, percentage)
   for prefix, percentage in grid],
  log_dir=f"eval_set_logs_1756388236.230403",
  model="openai/gpt-4o-mini-2024-07-18"
)
