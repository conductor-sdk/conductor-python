"""Conductor Workflow

The class in this module allows construction of a Conductor workflow in memory.
"""

from copy import deepcopy
from typing import Any, Dict, List, Union

from shortuuid import uuid
from typing_extensions import Self

from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.fork_task import ForkTask
from conductor.client.workflow.task.join_task import JoinTask
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.workflow.task.timeout_policy import TimeoutPolicy


class ConductorWorkflow:
    '''A class to create a conductor Workflow using a WorkflowExecutor.'''

    SCHEMA_VERSION = 2

    def __init__(
        self,
        executor: WorkflowExecutor,
        name: str,
        version: int = None,
        description: str = None,
    ) -> Self:
        self._executor = executor
        self.name = name
        self.version = version
        self.description = description
        self._tasks = []
        self._owner_email = None
        self._timeout_policy = None
        self._timeout_seconds = 60
        self._failure_workflow = ''
        self._input_parameters = []
        self._output_parameters = {}
        self._input_template = {}
        self._variables = {}
        self._restartable = True

    @property
    def name(self) -> str:
        """Gets the name of this Conductor Workflow.


        :return: The name of this Conductor Workflow.
        :rtype: str
        """

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of this ConductorWorkflow.


        :param name: The name of this ConductorWorkflow.
        :type: str
        """

        if not isinstance(name, str):
            raise Exception('invalid type')
        self._name = deepcopy(name)

    @property
    def version(self) -> int:
        """Gets the version of this Conductor Workflow.


        :return: The version of this Conductor Workflow.
        :rtype: int
        """

        return self._version

    @version.setter
    def version(self, version: int) -> None:
        """Sets the version of this ConductorWorkflow.


        :param version: The version of this ConductorWorkflow.
        :type: int
        """

        if version is not None and not isinstance(version, int):
            raise Exception('invalid type')
        self._version = deepcopy(version)

    @property
    def description(self) -> str:
        """Gets the description of this Conductor Workflow.


        :return: The description of this Conductor Workflow.
        :rtype: str
        """

        return self._description

    @description.setter
    def description(self, description: str) -> None:
        """Sets the description of this ConductorWorkflow.


        :param description: The description of this ConductorWorkflow.
        :type: str
        """

        if description is not None and not isinstance(description, str):
            raise Exception('invalid type')
        self._description = deepcopy(description)

    def timeout_policy(self, timeout_policy: TimeoutPolicy) -> Self:
        '''Sets the timeout policy on this Conductor workflow.'''

        if not isinstance(timeout_policy, TimeoutPolicy):
            raise Exception('invalid type')
        self._timeout_policy = deepcopy(timeout_policy)
        return self

    def timeout_seconds(self, timeout_seconds: int) -> Self:
        '''Sets the timeout in seconds on this Conductor workflow.'''

        if not isinstance(timeout_seconds, int):
            raise Exception('invalid type')
        self._timeout_seconds = deepcopy(timeout_seconds)
        return self

    def owner_email(self, owner_email: str) -> Self:
        '''Sets the owner email of this Conductor workflow.'''

        if not isinstance(owner_email, str):
            raise Exception('invalid type')
        self._owner_email = deepcopy(owner_email)
        return self

    def failure_workflow(self, failure_workflow: str) -> Self:
        """Sets the failure workflow to execute when this workflow fails.
        Failure workflows can be used for handling compensation logic.
        """

        if not isinstance(failure_workflow, str):
            raise Exception('invalid type')
        self._failure_workflow = deepcopy(failure_workflow)
        return self

    def restartable(self, restartable: bool) -> Self:
        """Sets the workflow as restartable so it can be allowed to restart
        after it has reached terminal state.
        Set this to false if restarting workflow can have side effects.
        """

        if not isinstance(restartable, bool):
            raise Exception('invalid type')
        self._restartable = deepcopy(restartable)
        return self

    def output_parameters(self, output_parameters: Dict[str, Any]) -> Self:
        """Sets the output parameters for the Conductor workflow.
        Workflow output follows similar structure as task input.
        See https://conductor.netflix.com/how-tos/Tasks/task-inputs.html."""

        if output_parameters is None:
            self._output_parameters = {}
            return self
        if not isinstance(output_parameters, dict):
            raise Exception('invalid type')
        for key in output_parameters.keys():
            if not isinstance(key, str):
                raise Exception('invalid type')
        self._output_parameters = deepcopy(output_parameters)
        return self

    def input_template(self, input_template: Dict[str, Any]) -> Self:
        """Sets an input template for the Conductor workflow. Can have
        combination of variables (e.g. ${workflow.input.abc}) and static values.
        """

        if input_template is None:
            self._input_template = {}
            return self
        if not isinstance(input_template, dict):
            raise Exception('invalid type')
        for key in input_template.keys():
            if not isinstance(key, str):
                raise Exception('invalid type')
        self._input_template = deepcopy(input_template)
        return self

    def variables(self, variables: Dict[str, Any]) -> Self:
        """Set the list of the variables in the conductor workflow.
        Variables are an excellent way to maintain business state.
        Variables can maintain business/user specific states which can be
        queried and inspected to find out the state of the workflow.
        They can be set using the SET_VARIABLE task.
        """

        if variables is None:
            self._variables = {}
            return self
        if not isinstance(variables, dict):
            raise Exception('invalid type')
        for key in variables.keys():
            if not isinstance(key, str):
                raise Exception('invalid type')
        self._variables = deepcopy(variables)
        return self

    def input_parameters(self, input_parameters: List[str]) -> Self:
        '''Set the list of the input parameters for the conductor workflow.'''

        if not isinstance(input_parameters, list):
            raise Exception('invalid type')
        for input_parameter in input_parameters:
            if not isinstance(input_parameter, str):
                raise Exception('invalid type')
        self._input_parameters = deepcopy(input_parameters)
        return self

    def register(self, overwrite: bool):
        """Register the workflow definition with the server.
        If overwrite is set, the definition on the server will be overwritten.
        When not set, the call fails if there is any change in the workflow
        definition between the server and what is being registered.
        """

        return self._executor.register_workflow(
            overwrite=overwrite,
            workflow=self.to_workflow_def(),
        )

    def start_workflow(self, start_workflow_request: StartWorkflowRequest):
        """Executes the workflow inline without registering with the server.
        Useful for one-off workflows that need not be registered.
        """

        start_workflow_request.workflow_def = self.to_workflow_def()
        return self._executor.start_workflow(start_workflow_request)

    def execute(
        self,
        workflow_input: dict,
        wait_until_task_ref: str = "",
        wait_for_seconds: int = 10,
    ) -> dict:
        """Executes the conductor workflow synchronously."""

        request = StartWorkflowRequest()
        request.workflow_def = self.to_workflow_def()
        request.input = workflow_input
        request.name = request.workflow_def.name
        request.version = 1
        run = self._executor.execute_workflow(
            request,
            wait_until_task_ref=wait_until_task_ref,
            wait_for_seconds=wait_for_seconds,
        )
        return run.output

    # Converts the workflow to the JSON serializable format
    def to_workflow_def(self) -> WorkflowDef:
        '''Converts the Conductor workflow to a Workflow Definition.'''

        return WorkflowDef(
            name=self._name,
            description=self._description,
            version=self._version,
            tasks=self.__get_workflow_task_list(),
            input_parameters=self._input_parameters,
            output_parameters=self._output_parameters,
            failure_workflow=self._failure_workflow,
            schema_version=ConductorWorkflow.SCHEMA_VERSION,
            owner_email=self._owner_email,
            timeout_policy=self._timeout_policy,
            timeout_seconds=self._timeout_seconds,
            variables=self._variables,
            input_template=self._input_template,
        )

    def __get_workflow_task_list(self) -> List[WorkflowTask]:
        workflow_task_list = []
        for task in self._tasks:
            converted_task = task.to_workflow_task()
            if isinstance(converted_task, list):
                for subtask in converted_task:
                    workflow_task_list.append(subtask)
            else:
                workflow_task_list.append(converted_task)
        return workflow_task_list

    # Append task with the right shift operator `>>`
    def __rshift__(
        self, task: Union[TaskInterface, List[TaskInterface], List[List[TaskInterface]]]
    ) -> Self:
        if isinstance(task, list):
            forked_tasks = []
            for fork_task in task:
                if isinstance(fork_task, list):
                    forked_tasks.append(fork_task)
                else:
                    forked_tasks.append([fork_task])
            return self.__add_fork_join_tasks(forked_tasks)
        return self.__add_task(task)

    def add(self, task: Union[TaskInterface, List[TaskInterface]]) -> Self:
        """Adds a list of tasks to the conductor workflow."""

        if isinstance(task, list):
            for t in task:
                self.__add_task(t)
            return self
        return self.__add_task(task)

    def __add_task(self, task: TaskInterface) -> Self:
        if not issubclass(type(task), TaskInterface):
            raise Exception('invalid type')
        self._tasks.append(deepcopy(task))
        return self

    def __add_fork_join_tasks(self, forked_tasks: List[List[TaskInterface]]) -> Self:
        for single_fork in forked_tasks:
            for task in single_fork:
                if not issubclass(type(task), TaskInterface):
                    raise Exception('invalid type')

        suffix = str(uuid())

        fork_task = ForkTask(
            task_ref_name="forked_" + suffix, forked_tasks=forked_tasks
        )

        join_task = JoinTask(
            task_ref_name="join_" + suffix, join_on=fork_task.to_workflow_task().join_on
        )

        self._tasks.append(fork_task)
        self._tasks.append(join_task)
        return self
