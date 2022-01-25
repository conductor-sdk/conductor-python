import abc


class WorkerInterface(abc.ABC):

    @abc.abstractmethod
    def get_task_definition_name(self):
        """Retrieve the name of the task definition the worker is currently working on.

        :return: TaskResult
        """
        pass

    @abc.abstractmethod
    def execute(self, task_result):
        """Executes a task and returns the updated task.

        :param TaskResult task: (required)
        :return: TaskResult
                 If the task is not completed yet, return with the status as IN_PROGRESS.
        """
        pass
