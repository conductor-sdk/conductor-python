from conductor.client.worker.worker_interface import WorkerInterface


class SimplePythonWorker(WorkerInterface):
    def execute(self, task):
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('key', 'value')
        task_result.status = 'COMPLETED'
        return task_result

    def get_polling_interval_in_seconds(self):
        return 1.5
