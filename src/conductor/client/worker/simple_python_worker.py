from conductor.client.worker.worker_interface import WorkerInterface
import multiprocessing
import socket


class SimplePythonWorker(WorkerInterface):
    def get_task_definition_name(self):
        return 'simple_python_worker'

    def execute(self, task_result):
        task_result.add_output_data('hostname', socket.gethostname())
        task_result.add_output_data('cpu_cores', multiprocessing.cpu_count())
        return task_result

    def get_polling_interval(self):
        return 3
