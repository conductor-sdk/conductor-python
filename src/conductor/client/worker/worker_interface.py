import abc
import socket


class WorkerInterface(abc.ABC):

    @abc.abstractmethod
    def get_task_definition_name(self):
        """Retrieve the name of the task definition the worker is currently working on.

        :return: TaskResult
        """
        pass

    @abc.abstractmethod
    def execute(self, task):
        """Executes a task and returns the updated task.

        :param Task task: (required)
        :return: TaskResult
                 If the task is not completed yet, return with the status as IN_PROGRESS.
        """
        pass

    @abc.abstractmethod
    def get_polling_interval(self):
        """Retrieve interval in seconds at which the server should be polled for worker tasks.

        :return: float
        """
        pass

    def get_identity(self):
        """Retrieve the hostname of the instance that the worker is running.

        :return: str
        """
        return socket.gethostname()
