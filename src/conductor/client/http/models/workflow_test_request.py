# coding: utf-8

import pprint
import re  # noqa: F401

import six


class WorkflowTestRequest(object):
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
        'correlation_id': 'str',
        'created_by': 'str',
        'external_input_payload_storage_path': 'str',
        'input': 'dict(str, object)',
        'name': 'str',
        'priority': 'int',
        'sub_workflow_test_request': 'dict(str, WorkflowTestRequest)',
        'task_ref_to_mock_output': 'dict(str, list[TaskMock])',
        'task_to_domain': 'dict(str, str)',
        'version': 'int',
        'workflow_def': 'WorkflowDef'
    }

    attribute_map = {
        'correlation_id': 'correlationId',
        'created_by': 'createdBy',
        'external_input_payload_storage_path': 'externalInputPayloadStoragePath',
        'input': 'input',
        'name': 'name',
        'priority': 'priority',
        'sub_workflow_test_request': 'subWorkflowTestRequest',
        'task_ref_to_mock_output': 'taskRefToMockOutput',
        'task_to_domain': 'taskToDomain',
        'version': 'version',
        'workflow_def': 'workflowDef'
    }

    def __init__(self, correlation_id=None, created_by=None, external_input_payload_storage_path=None, input=None,
                 name=None, priority=None, sub_workflow_test_request=None, task_ref_to_mock_output=None,
                 task_to_domain=None, version=None, workflow_def=None):  # noqa: E501
        """WorkflowTestRequest - a model defined in Swagger"""  # noqa: E501
        self._correlation_id = None
        self._created_by = None
        self._external_input_payload_storage_path = None
        self._input = None
        self._name = None
        self._priority = None
        self._sub_workflow_test_request = None
        self._task_ref_to_mock_output = None
        self._task_to_domain = None
        self._version = None
        self._workflow_def = None
        self.discriminator = None
        if correlation_id is not None:
            self.correlation_id = correlation_id
        if created_by is not None:
            self.created_by = created_by
        if external_input_payload_storage_path is not None:
            self.external_input_payload_storage_path = external_input_payload_storage_path
        if input is not None:
            self.input = input
        self.name = name
        if priority is not None:
            self.priority = priority
        if sub_workflow_test_request is not None:
            self.sub_workflow_test_request = sub_workflow_test_request
        if task_ref_to_mock_output is not None:
            self.task_ref_to_mock_output = task_ref_to_mock_output
        if task_to_domain is not None:
            self.task_to_domain = task_to_domain
        if version is not None:
            self.version = version
        if workflow_def is not None:
            self.workflow_def = workflow_def

    @property
    def correlation_id(self):
        """Gets the correlation_id of this WorkflowTestRequest.  # noqa: E501


        :return: The correlation_id of this WorkflowTestRequest.  # noqa: E501
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """Sets the correlation_id of this WorkflowTestRequest.


        :param correlation_id: The correlation_id of this WorkflowTestRequest.  # noqa: E501
        :type: str
        """

        self._correlation_id = correlation_id

    @property
    def created_by(self):
        """Gets the created_by of this WorkflowTestRequest.  # noqa: E501


        :return: The created_by of this WorkflowTestRequest.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this WorkflowTestRequest.


        :param created_by: The created_by of this WorkflowTestRequest.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def external_input_payload_storage_path(self):
        """Gets the external_input_payload_storage_path of this WorkflowTestRequest.  # noqa: E501


        :return: The external_input_payload_storage_path of this WorkflowTestRequest.  # noqa: E501
        :rtype: str
        """
        return self._external_input_payload_storage_path

    @external_input_payload_storage_path.setter
    def external_input_payload_storage_path(self, external_input_payload_storage_path):
        """Sets the external_input_payload_storage_path of this WorkflowTestRequest.


        :param external_input_payload_storage_path: The external_input_payload_storage_path of this WorkflowTestRequest.  # noqa: E501
        :type: str
        """

        self._external_input_payload_storage_path = external_input_payload_storage_path

    @property
    def input(self):
        """Gets the input of this WorkflowTestRequest.  # noqa: E501


        :return: The input of this WorkflowTestRequest.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this WorkflowTestRequest.


        :param input: The input of this WorkflowTestRequest.  # noqa: E501
        :type: dict(str, object)
        """

        self._input = input

    @property
    def name(self):
        """Gets the name of this WorkflowTestRequest.  # noqa: E501


        :return: The name of this WorkflowTestRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this WorkflowTestRequest.


        :param name: The name of this WorkflowTestRequest.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def priority(self):
        """Gets the priority of this WorkflowTestRequest.  # noqa: E501


        :return: The priority of this WorkflowTestRequest.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this WorkflowTestRequest.


        :param priority: The priority of this WorkflowTestRequest.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def sub_workflow_test_request(self):
        """Gets the sub_workflow_test_request of this WorkflowTestRequest.  # noqa: E501


        :return: The sub_workflow_test_request of this WorkflowTestRequest.  # noqa: E501
        :rtype: dict(str, WorkflowTestRequest)
        """
        return self._sub_workflow_test_request

    @sub_workflow_test_request.setter
    def sub_workflow_test_request(self, sub_workflow_test_request):
        """Sets the sub_workflow_test_request of this WorkflowTestRequest.


        :param sub_workflow_test_request: The sub_workflow_test_request of this WorkflowTestRequest.  # noqa: E501
        :type: dict(str, WorkflowTestRequest)
        """

        self._sub_workflow_test_request = sub_workflow_test_request

    @property
    def task_ref_to_mock_output(self):
        """Gets the task_ref_to_mock_output of this WorkflowTestRequest.  # noqa: E501


        :return: The task_ref_to_mock_output of this WorkflowTestRequest.  # noqa: E501
        :rtype: dict(str, list[TaskMock])
        """
        return self._task_ref_to_mock_output

    @task_ref_to_mock_output.setter
    def task_ref_to_mock_output(self, task_ref_to_mock_output):
        """Sets the task_ref_to_mock_output of this WorkflowTestRequest.


        :param task_ref_to_mock_output: The task_ref_to_mock_output of this WorkflowTestRequest.  # noqa: E501
        :type: dict(str, list[TaskMock])
        """

        self._task_ref_to_mock_output = task_ref_to_mock_output

    @property
    def task_to_domain(self):
        """Gets the task_to_domain of this WorkflowTestRequest.  # noqa: E501


        :return: The task_to_domain of this WorkflowTestRequest.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._task_to_domain

    @task_to_domain.setter
    def task_to_domain(self, task_to_domain):
        """Sets the task_to_domain of this WorkflowTestRequest.


        :param task_to_domain: The task_to_domain of this WorkflowTestRequest.  # noqa: E501
        :type: dict(str, str)
        """

        self._task_to_domain = task_to_domain

    @property
    def version(self):
        """Gets the version of this WorkflowTestRequest.  # noqa: E501


        :return: The version of this WorkflowTestRequest.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this WorkflowTestRequest.


        :param version: The version of this WorkflowTestRequest.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def workflow_def(self):
        """Gets the workflow_def of this WorkflowTestRequest.  # noqa: E501


        :return: The workflow_def of this WorkflowTestRequest.  # noqa: E501
        :rtype: WorkflowDef
        """
        return self._workflow_def

    @workflow_def.setter
    def workflow_def(self, workflow_def):
        """Sets the workflow_def of this WorkflowTestRequest.


        :param workflow_def: The workflow_def of this WorkflowTestRequest.  # noqa: E501
        :type: WorkflowDef
        """

        self._workflow_def = workflow_def

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
        if issubclass(WorkflowTestRequest, dict):
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
        if not isinstance(other, WorkflowTestRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
