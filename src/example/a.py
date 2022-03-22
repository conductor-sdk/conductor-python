from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.http.models import Task, TaskResult
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from pathlib import Path
import logging
import os

# Create a Simple Python Worker
class SimplePythonWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('key1', 'value')
        task_result.add_output_data('key2', 42)
        task_result.add_output_data('key3', False)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result
    
def main():
    
    # Create a temp folder for metrics logs
    metrics_dir = str(Path.home()) + '/tmp/'
    if not os.path.isdir(metrics_dir):
        os.mkdir(metrics_dir)

    metrics_settings = MetricsSettings(
        directory=metrics_dir
    )

    # Optionally, if you are using Conductor server that requires authentication,  setup key_id and secret
    auth=AuthenticationSettings(
        key_id='id',
        key_secret='secret'
    )
    
    # Point to the Conductor Server
    configuration = Configuration(
        base_url='http://localhost:8080',
	debug=True,
        # authentication_settings=auth      # Optional if you are using server that requires authentication
    )
    
    # Add two workers 
    workers = [
        SimplePythonWorker('python_task')
    ]
    
    # Start the worker processes and wait
    with TaskHandler(workers, configuration=configuration, metrics_settings=metrics_settings) as task_handler:
        task_handler.start_processes()
        task_handler.join_processes()


if __name__ == '__main__':
    main()

