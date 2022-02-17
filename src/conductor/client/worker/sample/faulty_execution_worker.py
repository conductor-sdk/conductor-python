from conductor.client.worker.worker_interface import WorkerInterface


class FaultyExecutionWorker(WorkerInterface):
    def __init__(self):
        super().__init__('faulty_execution_worker')

    def execute(self, task):
        raise Exception('faulty execution')
