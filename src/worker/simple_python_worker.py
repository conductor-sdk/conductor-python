from src.worker.worker_interface import WorkerInterface
import socket


class SimplePythonWorker(WorkerInterface):
    def get_task_definition_name(self):
        return 'simple_python_worker'

    def execute(self, task_result):
        task_result.add_output_data('hostname', socket.gethostname())
        return task_result
