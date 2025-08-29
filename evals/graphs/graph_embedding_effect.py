import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from uuid import UUID

from attack import locations

T = TypeVar("T")


def from_str(x: Any) -> str:
  assert isinstance(x, str)
  return x


def from_float(x: Any) -> float:
  assert isinstance(x, (float, int)) and not isinstance(x, bool)
  return float(x)


def to_float(x: Any) -> float:
  assert isinstance(x, (int, float))
  return x


def to_class(c: Type[T], x: Any) -> dict:
  assert isinstance(x, c)
  return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
  assert isinstance(x, list)
  return [f(y) for y in x]


@dataclass
class Metadata:
  employee: str
  percentage_of_rag_emails_to_fetch: float
  prefix: str

  @staticmethod
  def from_dict(obj: Any) -> 'Metadata':
    assert isinstance(obj, dict)
    employee = from_str(obj.get("employee"))
    percentage_of_rag_emails_to_fetch = from_float(obj.get("percentage_of_rag_emails_to_fetch"))
    prefix = from_str(obj.get("prefix"))
    return Metadata(employee, percentage_of_rag_emails_to_fetch, prefix)

  def to_dict(self) -> dict:
    result: dict = {}
    result["employee"] = from_str(self.employee)
    result["percentage_of_rag_emails_to_fetch"] = to_float(self.percentage_of_rag_emails_to_fetch)
    result["prefix"] = from_str(self.prefix)
    return result


@dataclass
class PromptDatum:
  id: UUID
  input: str
  metadata: Metadata
  target: str

  @staticmethod
  def from_dict(obj: Any) -> 'PromptDatum':
    assert isinstance(obj, dict)
    id = UUID(obj.get("id"))
    input = from_str(obj.get("input"))
    metadata = Metadata.from_dict(obj.get("metadata"))
    target = from_str(obj.get("target"))
    return PromptDatum(id, input, metadata, target)

  def to_dict(self) -> dict:
    result: dict = {}
    result["id"] = str(self.id)
    result["input"] = from_str(self.input)
    result["metadata"] = to_class(Metadata, self.metadata)
    result["target"] = from_str(self.target)
    return result


def prompt_data_from_dict(s: Any) -> List[PromptDatum]:
  return from_list(PromptDatum.from_dict, s)


def prompt_data_to_dict(x: List[PromptDatum]) -> Any:
  return from_list(lambda x: to_class(PromptDatum, x), x)


def load_prefix_log():
  prefix_log_dir = locations.current_path / "evals" / "inspect"

  datasets = [
    "gte-base_dataset.json",
    "gte-large_dataset.json",
    "gte-small_dataset.json",
  ]

  results_by_file = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

  for file in datasets:
    filepath = prefix_log_dir / file
    with open(filepath) as f:
      j = json.load(f)
      prompt_data = prompt_data_from_dict(j)
      for prompt in prompt_data:
        kind = ("prefix", prompt.metadata.percentage_of_rag_emails_to_fetch)
        if "Wormy" in prompt.input:
          results_by_file[file][kind]["success"] += 1
        else:
          results_by_file[file][kind]["failure"] += 1

  print(results_by_file)


if __name__ == '__main__':
  load_prefix_log()
