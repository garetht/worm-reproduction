from inspect_ai.log import read_eval_log, list_eval_logs, EvalLog

from attack import locations


def load_prefix_log():
  prefix_log_dir = locations.current_path / "eval_worm_prefix_replication"
  all_eval_logs = list_eval_logs(str(prefix_log_dir))

  eval_logs: list[EvalLog] = []
  for eval_log in all_eval_logs:
    eval_logs.append(read_eval_log(eval_log, header_only=True))

  for log in eval_logs:
    print(log.eval.task_args)
    print(log.results.scores[0].metrics["accuracy"].value)

if __name__ == '__main__':
    load_prefix_log()


