from conductor.client.automator.task_runner import TaskRunner
import multiprocessing


class TaskHandler:
    task_runner_processes = []

    def __init__(self, workers):
        for worker in workers:
            task_runner = TaskRunner(worker)
            process = multiprocessing.Process(
                target=task_runner.run
            )
            self.task_runner_processes.append(process)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for task_runner_process in self.task_runner_processes:
            try:
                task_runner_process.kill()
            except Exception as e:
                task_runner_process.terminate()

    def start(self):
        for task_runner_process in self.task_runner_processes:
            task_runner_process.start()
        for task_runner_process in self.task_runner_processes:
            task_runner_process.join()
