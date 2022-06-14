from __future__ import annotations
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task import TaskInterface
from typing import Any, Dict, List
from .timeout_policy import TimeoutPolicy


class ConductorWorkflow:
    executor: WorkflowExecutor
    name: str
    version: int
    description: str
    owner_email: str
    tasks: List[TaskInterface]
    timeout_policy: TimeoutPolicy
    timeout_seconds: int
    failure_workflow: str
    input_parameters: List[str]
    output_parameters: Dict[str, Any]
    input_template: Dict[str, Any]
    variables: Dict[str, Any]
    restartable: bool

    def __init__(self, executor: WorkflowExecutor) -> ConductorWorkflow:
        self.executor = executor
        self.tasks = []

    def Name(self, name: str) -> ConductorWorkflow:
        self.name = name
        return self

    def Version(self, version: int) -> ConductorWorkflow:
        self.version = version
        return self

    def Description(self, description: str) -> ConductorWorkflow:
        self.description = description
        return self

    def TimeoutSeconds(self, timeout_seconds: int) -> ConductorWorkflow:
        self.timeout_seconds = timeout_seconds
        return self

    def OwnerEmail(self, owner_email: str) -> ConductorWorkflow:
        self.owner_email = owner_email
        return self

    # FailureWorkflow name of the workflow to execute when this workflow fails.
    # Failure workflows can be used for handling compensation logic
    def FailureWorkflow(self, failure_workflow: str) -> ConductorWorkflow:
        self.failure_workflow = failure_workflow
        return self

    # Restartable if the workflow can be restarted after it has reached terminal state.
    # Set this to false if restarting workflow can have side effects
    def Restartable(self, restartable: bool) -> ConductorWorkflow:
        self.restartable = restartable
        return self

    # OutputParameters Workflow outputs. Workflow output follows similar structure as task inputs
    # See https://conductor.netflix.com/how-tos/Tasks/task-inputs.html for more details
    def OutputParameters(self, output_parameters: Dict[str, Any]) -> ConductorWorkflow:
        self.output_parameters = output_parameters
        return self

    # InputTemplate template input to the workflow.  Can have combination of variables (e.g. ${workflow.input.abc}) and static values
    def InputTemplate(self, input_template: Dict[str, Any]) -> ConductorWorkflow:
        self.input_template = input_template
        return self

    # Variables Workflow variables are set using SET_VARIABLE task. Excellent way to maintain business state
    # e.g. Variables can maintain business/user specific states which can be queried and inspected to find out the state of the workflow
    def Variables(self, variables: Dict[str, Any]) -> ConductorWorkflow:
        self.variables = variables
        return self

    # InputParameters List of the input parameters to the workflow.  Used ONLY for the documentation purpose.
    def InputParameters(self, input_parameters: List[str]) -> ConductorWorkflow:
        self.input_parameters = input_parameters
        return self

    def Add(self, task: TaskInterface) -> ConductorWorkflow:
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
            name=self.name,
            description=self.description,
            version=self.version,
            tasks=self.tasks,
            input_parameters=self.input_parameters,
            output_parameters=self.output_parameters,
            failure_workflow=self.failure_workflow,
            schema_version=2,
            owner_email=self.owner_email,
            timeout_policy=self.timeout_policy,
            timeout_seconds=self.timeout_seconds,
            variables=self.variables,
            input_template=self.input_template,
        )
