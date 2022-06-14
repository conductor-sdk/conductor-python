from __future__ import annotations
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task import TaskInterface
from conductor.client.workflow.timeout_policy import TimeoutPolicy
from typing import Any, Dict, List


class ConductorWorkflow:
    SCHEMA_VERSION = 2

    _executor: WorkflowExecutor
    _name: str
    _version: int
    _description: str
    _owner_email: str
    _tasks: List[TaskInterface]
    _timeout_policy: TimeoutPolicy
    _timeout_seconds: int
    _failure_workflow: str
    _input_parameters: List[str]
    _output_parameters: Dict[str, Any]
    _input_template: Dict[str, Any]
    _variables: Dict[str, Any]
    _restartable: bool

    def __init__(self, executor: WorkflowExecutor) -> ConductorWorkflow:
        self.executor = executor
        self.tasks = []

    def name(self, name: str) -> ConductorWorkflow:
        if not isinstance(name, str):
            raise Exception('invalid type')
        self._name = name
        return self

    def version(self, version: int) -> ConductorWorkflow:
        if not isinstance(version, str):
            raise Exception('invalid type')
        self._version = version
        return self

    def description(self, description: str) -> ConductorWorkflow:
        if not isinstance(description, str):
            raise Exception('invalid type')
        self._description = description
        return self

    def timeout_policy(self, timeout_policy: TimeoutPolicy) -> ConductorWorkflow:
        if not isinstance(timeout_policy, TimeoutPolicy):
            raise Exception('invalid type')
        self._timeout_policy = timeout_policy
        return self

    def timeout_seconds(self, timeout_seconds: int) -> ConductorWorkflow:
        if not isinstance(timeout_seconds, int):
            raise Exception('invalid type')
        self._timeout_seconds = timeout_seconds
        return self

    def owner_email(self, owner_email: str) -> ConductorWorkflow:
        if not isinstance(owner_email, str):
            raise Exception('invalid type')
        self._owner_email = owner_email
        return self

    # Name of the workflow to execute when this workflow fails.
    # Failure workflows can be used for handling compensation logic
    def failure_workflow(self, failure_workflow: str) -> ConductorWorkflow:
        if not isinstance(failure_workflow, str):
            raise Exception('invalid type')
        self._failure_workflow = failure_workflow
        return self

    # If the workflow can be restarted after it has reached terminal state.
    # Set this to false if restarting workflow can have side effects
    def restartable(self, restartable: bool) -> ConductorWorkflow:
        if not isinstance(restartable, bool):
            raise Exception('invalid type')
        self._restartable = restartable
        return self

    # Workflow output follows similar structure as task input
    # See https://conductor.netflix.com/how-tos/Tasks/task-inputs.html for more details
    def output_parameters(self, output_parameters: Dict[str, Any]) -> ConductorWorkflow:
        # TODO validate dict type
        self._output_parameters = output_parameters
        return self

    # InputTemplate template input to the workflow.  Can have combination of variables (e.g. ${workflow.input.abc}) and static values
    def input_template(self, input_template: Dict[str, Any]) -> ConductorWorkflow:
        # TODO validate dict type
        self._input_template = input_template
        return self

    # Variables are set using SET_VARIABLE task. Excellent way to maintain business state
    # e.g. Variables can maintain business/user specific states which can be queried and inspected to find out the state of the workflow
    def variables(self, variables: Dict[str, Any]) -> ConductorWorkflow:
        # TODO validate dict type
        self._variables = variables
        return self

    # List of the input parameters to the workflow. Usage: documentation ONLY
    def input_parameters(self, input_parameters: List[str]) -> ConductorWorkflow:
        if not isinstance(input_parameters, list):
            raise Exception('invalid type')
        for input_parameter in input_parameters:
            if not isinstance(input_parameter, str):
                raise Exception('invalid type')
        self._input_parameters = input_parameters
        return self

    def add(self, task: TaskInterface) -> ConductorWorkflow:
        if not issubclass(task, TaskInterface):
            raise Exception('invalid type')
        self.tasks.append(task)
        return self

    # Register the workflow definition with the server. If overwrite is set, the definition on the server will be overwritten.
    # When not set, the call fails if there is any change in the workflow definition between the server and what is being registered.
    def register(self, overwrite: bool):
        return self.executor.register_workflow(
            overwrite=overwrite,
            workflow=self.to_workflow_def(),
        )

    # Converts the workflow to the JSON serializable format
    def to_workflow_def(self) -> WorkflowDef:
        return WorkflowDef(
            name=self._name,
            description=self._description,
            version=self._version,
            tasks=self.tasks,
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
