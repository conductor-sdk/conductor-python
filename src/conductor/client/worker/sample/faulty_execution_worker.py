from conductor.client.worker.worker_interface import WorkerInterface


class FaultyExecutionWorker(WorkerInterface):
    def execute(self, task):
        raise Exception('faulty execution')
