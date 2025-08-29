# Tests the effect of various prefixes on worm retrieval success rate
from datetime import datetime

from inspect_ai import task, Task, eval_set
from inspect_ai.solver import solver, TaskState, Generate
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import match
from inspect_ai.model import ModelOutput

from evals.inspect.prefix_generate_dataset import generate_grid
from prompts.prefixes import PrefixPrompts


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
eval_grid = generate_grid()

# run the evals and capture the logs
success, logs = eval_set(
  [
    rag_worm_retrieval_detection(prefix, percentage, embedding_type)
    for prefix, percentage, embedding_type in eval_grid
  ],
  log_dir=f"eval_set_logs_{unix_timestamp}",
  model="openai/gpt-4o-mini-2024-07-18"
)
