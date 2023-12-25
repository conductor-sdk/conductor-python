import pprint
import re  # noqa: F401

import six

class Workflow(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'owner_app': 'str',
        'create_time': 'int',
        'update_time': 'int',
        'created_by': 'str',
        'updated_by': 'str',
        'status': 'str',
        'end_time': 'int',
        'workflow_id': 'str',
        'parent_workflow_id': 'str',
        'parent_workflow_task_id': 'str',
        'tasks': 'list[Task]',
        'input': 'dict(str, object)',
        'output': 'dict(str, object)',
        'correlation_id': 'str',
        're_run_from_workflow_id': 'str',
        'reason_for_incompletion': 'str',
        'event': 'str',
        'task_to_domain': 'dict(str, str)',
        'failed_reference_task_names': 'list[str]',
        'workflow_definition': 'WorkflowDef',
        'external_input_payload_storage_path': 'str',
        'external_output_payload_storage_path': 'str',
        'priority': 'int',
        'variables': 'dict(str, object)',
        'last_retried_time': 'int',
        'start_time': 'int',
        'workflow_name': 'str',
        'workflow_version': 'int'
    }

    attribute_map = {
        'owner_app': 'ownerApp',
        'create_time': 'createTime',
        'update_time': 'updateTime',
        'created_by': 'createdBy',
        'updated_by': 'updatedBy',
        'status': 'status',
        'end_time': 'endTime',
        'workflow_id': 'workflowId',
        'parent_workflow_id': 'parentWorkflowId',
        'parent_workflow_task_id': 'parentWorkflowTaskId',
        'tasks': 'tasks',
        'input': 'input',
        'output': 'output',
        'correlation_id': 'correlationId',
        're_run_from_workflow_id': 'reRunFromWorkflowId',
        'reason_for_incompletion': 'reasonForIncompletion',
        'event': 'event',
        'task_to_domain': 'taskToDomain',
        'failed_reference_task_names': 'failedReferenceTaskNames',
        'workflow_definition': 'workflowDefinition',
        'external_input_payload_storage_path': 'externalInputPayloadStoragePath',
        'external_output_payload_storage_path': 'externalOutputPayloadStoragePath',
        'priority': 'priority',
        'variables': 'variables',
        'last_retried_time': 'lastRetriedTime',
        'start_time': 'startTime',
        'workflow_name': 'workflowName',
        'workflow_version': 'workflowVersion'
    }

    def __init__(self, owner_app=None, create_time=None, update_time=None, created_by=None, updated_by=None, status=None, end_time=None, workflow_id=None, parent_workflow_id=None, parent_workflow_task_id=None, tasks=None, input=None, output=None, correlation_id=None, re_run_from_workflow_id=None, reason_for_incompletion=None, event=None, task_to_domain=None, failed_reference_task_names=None, workflow_definition=None, external_input_payload_storage_path=None, external_output_payload_storage_path=None, priority=None, variables=None, last_retried_time=None, start_time=None, workflow_name=None, workflow_version=None):  # noqa: E501
        """Workflow - a model defined in Swagger"""  # noqa: E501
        self._owner_app = None
        self._create_time = None
        self._update_time = None
        self._created_by = None
        self._updated_by = None
        self._status = None
        self._end_time = None
        self._workflow_id = None
        self._parent_workflow_id = None
        self._parent_workflow_task_id = None
        self._tasks = None
        self._input = None
        self._output = None
        self._correlation_id = None
        self._re_run_from_workflow_id = None
        self._reason_for_incompletion = None
        self._event = None
        self._task_to_domain = None
        self._failed_reference_task_names = None
        self._workflow_definition = None
        self._external_input_payload_storage_path = None
        self._external_output_payload_storage_path = None
        self._priority = None
        self._variables = None
        self._last_retried_time = None
        self._start_time = None
        self._workflow_name = None
        self._workflow_version = None
        self.discriminator = None
        if owner_app is not None:
            self.owner_app = owner_app
        if create_time is not None:
            self.create_time = create_time
        if update_time is not None:
            self.update_time = update_time
        if created_by is not None:
            self.created_by = created_by
        if updated_by is not None:
            self.updated_by = updated_by
        if status is not None:
            self.status = status
        if end_time is not None:
            self.end_time = end_time
        if workflow_id is not None:
            self.workflow_id = workflow_id
        if parent_workflow_id is not None:
            self.parent_workflow_id = parent_workflow_id
        if parent_workflow_task_id is not None:
            self.parent_workflow_task_id = parent_workflow_task_id
        if tasks is not None:
            self.tasks = tasks
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output
        if correlation_id is not None:
            self.correlation_id = correlation_id
        if re_run_from_workflow_id is not None:
            self.re_run_from_workflow_id = re_run_from_workflow_id
        if reason_for_incompletion is not None:
            self.reason_for_incompletion = reason_for_incompletion
        if event is not None:
            self.event = event
        if task_to_domain is not None:
            self.task_to_domain = task_to_domain
        if failed_reference_task_names is not None:
            self.failed_reference_task_names = failed_reference_task_names
        if workflow_definition is not None:
            self.workflow_definition = workflow_definition
        if external_input_payload_storage_path is not None:
            self.external_input_payload_storage_path = external_input_payload_storage_path
        if external_output_payload_storage_path is not None:
            self.external_output_payload_storage_path = external_output_payload_storage_path
        if priority is not None:
            self.priority = priority
        if variables is not None:
            self.variables = variables
        if last_retried_time is not None:
            self.last_retried_time = last_retried_time
        if start_time is not None:
            self.start_time = start_time
        if workflow_name is not None:
            self.workflow_name = workflow_name
        if workflow_version is not None:
            self.workflow_version = workflow_version

    @property
    def owner_app(self):
        """Gets the owner_app of this Workflow.  # noqa: E501


        :return: The owner_app of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._owner_app

    @owner_app.setter
    def owner_app(self, owner_app):
        """Sets the owner_app of this Workflow.


        :param owner_app: The owner_app of this Workflow.  # noqa: E501
        :type: str
        """

        self._owner_app = owner_app

    @property
    def create_time(self):
        """Gets the create_time of this Workflow.  # noqa: E501


        :return: The create_time of this Workflow.  # noqa: E501
        :rtype: int
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this Workflow.


        :param create_time: The create_time of this Workflow.  # noqa: E501
        :type: int
        """

        self._create_time = create_time

    @property
    def update_time(self):
        """Gets the update_time of this Workflow.  # noqa: E501


        :return: The update_time of this Workflow.  # noqa: E501
        :rtype: int
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this Workflow.


        :param update_time: The update_time of this Workflow.  # noqa: E501
        :type: int
        """

        self._update_time = update_time

    @property
    def created_by(self):
        """Gets the created_by of this Workflow.  # noqa: E501


        :return: The created_by of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Workflow.


        :param created_by: The created_by of this Workflow.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def updated_by(self):
        """Gets the updated_by of this Workflow.  # noqa: E501


        :return: The updated_by of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this Workflow.


        :param updated_by: The updated_by of this Workflow.  # noqa: E501
        :type: str
        """

        self._updated_by = updated_by

    @property
    def status(self) -> str:
        """Gets the status of this Workflow.  # noqa: E501


        :return: The status of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Workflow.


        :param status: The status of this Workflow.  # noqa: E501
        :type: str
        """
        allowed_values = ["RUNNING", "COMPLETED", "FAILED", "TIMED_OUT", "TERMINATED", "PAUSED"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def end_time(self):
        """Gets the end_time of this Workflow.  # noqa: E501


        :return: The end_time of this Workflow.  # noqa: E501
        :rtype: int
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this Workflow.


        :param end_time: The end_time of this Workflow.  # noqa: E501
        :type: int
        """

        self._end_time = end_time

    @property
    def workflow_id(self):
        """Gets the workflow_id of this Workflow.  # noqa: E501


        :return: The workflow_id of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        """Sets the workflow_id of this Workflow.


        :param workflow_id: The workflow_id of this Workflow.  # noqa: E501
        :type: str
        """

        self._workflow_id = workflow_id

    @property
    def parent_workflow_id(self):
        """Gets the parent_workflow_id of this Workflow.  # noqa: E501


        :return: The parent_workflow_id of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._parent_workflow_id

    @parent_workflow_id.setter
    def parent_workflow_id(self, parent_workflow_id):
        """Sets the parent_workflow_id of this Workflow.


        :param parent_workflow_id: The parent_workflow_id of this Workflow.  # noqa: E501
        :type: str
        """

        self._parent_workflow_id = parent_workflow_id

    @property
    def parent_workflow_task_id(self):
        """Gets the parent_workflow_task_id of this Workflow.  # noqa: E501


        :return: The parent_workflow_task_id of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._parent_workflow_task_id

    @parent_workflow_task_id.setter
    def parent_workflow_task_id(self, parent_workflow_task_id):
        """Sets the parent_workflow_task_id of this Workflow.


        :param parent_workflow_task_id: The parent_workflow_task_id of this Workflow.  # noqa: E501
        :type: str
        """

        self._parent_workflow_task_id = parent_workflow_task_id

    @property
    def tasks(self):
        """Gets the tasks of this Workflow.  # noqa: E501


        :return: The tasks of this Workflow.  # noqa: E501
        :rtype: list[Task]
        """
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        """Sets the tasks of this Workflow.


        :param tasks: The tasks of this Workflow.  # noqa: E501
        :type: list[Task]
        """

        self._tasks = tasks

    @property
    def input(self):
        """Gets the input of this Workflow.  # noqa: E501


        :return: The input of this Workflow.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this Workflow.


        :param input: The input of this Workflow.  # noqa: E501
        :type: dict(str, object)
        """

        self._input = input

    @property
    def output(self):
        """Gets the output of this Workflow.  # noqa: E501


        :return: The output of this Workflow.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this Workflow.


        :param output: The output of this Workflow.  # noqa: E501
        :type: dict(str, object)
        """

        self._output = output

    @property
    def correlation_id(self):
        """Gets the correlation_id of this Workflow.  # noqa: E501


        :return: The correlation_id of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """Sets the correlation_id of this Workflow.


        :param correlation_id: The correlation_id of this Workflow.  # noqa: E501
        :type: str
        """

        self._correlation_id = correlation_id

    @property
    def re_run_from_workflow_id(self):
        """Gets the re_run_from_workflow_id of this Workflow.  # noqa: E501


        :return: The re_run_from_workflow_id of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._re_run_from_workflow_id

    @re_run_from_workflow_id.setter
    def re_run_from_workflow_id(self, re_run_from_workflow_id):
        """Sets the re_run_from_workflow_id of this Workflow.


        :param re_run_from_workflow_id: The re_run_from_workflow_id of this Workflow.  # noqa: E501
        :type: str
        """

        self._re_run_from_workflow_id = re_run_from_workflow_id

    @property
    def reason_for_incompletion(self):
        """Gets the reason_for_incompletion of this Workflow.  # noqa: E501


        :return: The reason_for_incompletion of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._reason_for_incompletion

    @reason_for_incompletion.setter
    def reason_for_incompletion(self, reason_for_incompletion):
        """Sets the reason_for_incompletion of this Workflow.


        :param reason_for_incompletion: The reason_for_incompletion of this Workflow.  # noqa: E501
        :type: str
        """

        self._reason_for_incompletion = reason_for_incompletion

    @property
    def event(self):
        """Gets the event of this Workflow.  # noqa: E501


        :return: The event of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._event

    @event.setter
    def event(self, event):
        """Sets the event of this Workflow.


        :param event: The event of this Workflow.  # noqa: E501
        :type: str
        """

        self._event = event

    @property
    def task_to_domain(self):
        """Gets the task_to_domain of this Workflow.  # noqa: E501


        :return: The task_to_domain of this Workflow.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._task_to_domain

    @task_to_domain.setter
    def task_to_domain(self, task_to_domain):
        """Sets the task_to_domain of this Workflow.


        :param task_to_domain: The task_to_domain of this Workflow.  # noqa: E501
        :type: dict(str, str)
        """

        self._task_to_domain = task_to_domain

    @property
    def failed_reference_task_names(self):
        """Gets the failed_reference_task_names of this Workflow.  # noqa: E501


        :return: The failed_reference_task_names of this Workflow.  # noqa: E501
        :rtype: list[str]
        """
        return self._failed_reference_task_names

    @failed_reference_task_names.setter
    def failed_reference_task_names(self, failed_reference_task_names):
        """Sets the failed_reference_task_names of this Workflow.


        :param failed_reference_task_names: The failed_reference_task_names of this Workflow.  # noqa: E501
        :type: list[str]
        """

        self._failed_reference_task_names = failed_reference_task_names

    @property
    def workflow_definition(self):
        """Gets the workflow_definition of this Workflow.  # noqa: E501


        :return: The workflow_definition of this Workflow.  # noqa: E501
        :rtype: WorkflowDef
        """
        return self._workflow_definition

    @workflow_definition.setter
    def workflow_definition(self, workflow_definition):
        """Sets the workflow_definition of this Workflow.


        :param workflow_definition: The workflow_definition of this Workflow.  # noqa: E501
        :type: WorkflowDef
        """

        self._workflow_definition = workflow_definition

    @property
    def external_input_payload_storage_path(self):
        """Gets the external_input_payload_storage_path of this Workflow.  # noqa: E501


        :return: The external_input_payload_storage_path of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._external_input_payload_storage_path

    @external_input_payload_storage_path.setter
    def external_input_payload_storage_path(self, external_input_payload_storage_path):
        """Sets the external_input_payload_storage_path of this Workflow.


        :param external_input_payload_storage_path: The external_input_payload_storage_path of this Workflow.  # noqa: E501
        :type: str
        """

        self._external_input_payload_storage_path = external_input_payload_storage_path

    @property
    def external_output_payload_storage_path(self):
        """Gets the external_output_payload_storage_path of this Workflow.  # noqa: E501


        :return: The external_output_payload_storage_path of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._external_output_payload_storage_path

    @external_output_payload_storage_path.setter
    def external_output_payload_storage_path(self, external_output_payload_storage_path):
        """Sets the external_output_payload_storage_path of this Workflow.


        :param external_output_payload_storage_path: The external_output_payload_storage_path of this Workflow.  # noqa: E501
        :type: str
        """

        self._external_output_payload_storage_path = external_output_payload_storage_path

    @property
    def priority(self):
        """Gets the priority of this Workflow.  # noqa: E501


        :return: The priority of this Workflow.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this Workflow.


        :param priority: The priority of this Workflow.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def variables(self):
        """Gets the variables of this Workflow.  # noqa: E501


        :return: The variables of this Workflow.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._variables

    @variables.setter
    def variables(self, variables):
        """Sets the variables of this Workflow.


        :param variables: The variables of this Workflow.  # noqa: E501
        :type: dict(str, object)
        """

        self._variables = variables

    @property
    def last_retried_time(self):
        """Gets the last_retried_time of this Workflow.  # noqa: E501


        :return: The last_retried_time of this Workflow.  # noqa: E501
        :rtype: int
        """
        return self._last_retried_time

    @last_retried_time.setter
    def last_retried_time(self, last_retried_time):
        """Sets the last_retried_time of this Workflow.


        :param last_retried_time: The last_retried_time of this Workflow.  # noqa: E501
        :type: int
        """

        self._last_retried_time = last_retried_time

    @property
    def start_time(self):
        """Gets the start_time of this Workflow.  # noqa: E501


        :return: The start_time of this Workflow.  # noqa: E501
        :rtype: int
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this Workflow.


        :param start_time: The start_time of this Workflow.  # noqa: E501
        :type: int
        """

        self._start_time = start_time

    @property
    def workflow_name(self):
        """Gets the workflow_name of this Workflow.  # noqa: E501


        :return: The workflow_name of this Workflow.  # noqa: E501
        :rtype: str
        """
        return self._workflow_name

    @workflow_name.setter
    def workflow_name(self, workflow_name):
        """Sets the workflow_name of this Workflow.


        :param workflow_name: The workflow_name of this Workflow.  # noqa: E501
        :type: str
        """

        self._workflow_name = workflow_name

    @property
    def workflow_version(self):
        """Gets the workflow_version of this Workflow.  # noqa: E501


        :return: The workflow_version of this Workflow.  # noqa: E501
        :rtype: int
        """
        return self._workflow_version

    @workflow_version.setter
    def workflow_version(self, workflow_version):
        """Sets the workflow_version of this Workflow.


        :param workflow_version: The workflow_version of this Workflow.  # noqa: E501
        :type: int
        """

        self._workflow_version = workflow_version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Workflow, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Workflow):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
