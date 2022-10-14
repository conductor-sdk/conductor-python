import pprint
import re  # noqa: F401

import six

class WorkflowStatus(object):
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
        'output': 'dict(str, object)',
        'status': 'str',
        'variables': 'dict(str, object)',
        'workflow_id': 'str'
    }

    attribute_map = {
        'correlation_id': 'correlationId',
        'output': 'output',
        'status': 'status',
        'variables': 'variables',
        'workflow_id': 'workflowId'
    }

    def __init__(self, correlation_id=None, output=None, status=None, variables=None, workflow_id=None):  # noqa: E501
        """WorkflowStatus - a model defined in Swagger"""  # noqa: E501
        self._correlation_id = None
        self._output = None
        self._status = None
        self._variables = None
        self._workflow_id = None
        self.discriminator = None
        if correlation_id is not None:
            self.correlation_id = correlation_id
        if output is not None:
            self.output = output
        if status is not None:
            self.status = status
        if variables is not None:
            self.variables = variables
        if workflow_id is not None:
            self.workflow_id = workflow_id

    @property
    def correlation_id(self):
        """Gets the correlation_id of this WorkflowStatus.  # noqa: E501


        :return: The correlation_id of this WorkflowStatus.  # noqa: E501
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """Sets the correlation_id of this WorkflowStatus.


        :param correlation_id: The correlation_id of this WorkflowStatus.  # noqa: E501
        :type: str
        """

        self._correlation_id = correlation_id

    @property
    def output(self):
        """Gets the output of this WorkflowStatus.  # noqa: E501


        :return: The output of this WorkflowStatus.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this WorkflowStatus.


        :param output: The output of this WorkflowStatus.  # noqa: E501
        :type: dict(str, object)
        """

        self._output = output

    @property
    def status(self):
        """Gets the status of this WorkflowStatus.  # noqa: E501


        :return: The status of this WorkflowStatus.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this WorkflowStatus.


        :param status: The status of this WorkflowStatus.  # noqa: E501
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
    def variables(self):
        """Gets the variables of this WorkflowStatus.  # noqa: E501


        :return: The variables of this WorkflowStatus.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._variables

    @variables.setter
    def variables(self, variables):
        """Sets the variables of this WorkflowStatus.


        :param variables: The variables of this WorkflowStatus.  # noqa: E501
        :type: dict(str, object)
        """

        self._variables = variables

    @property
    def workflow_id(self):
        """Gets the workflow_id of this WorkflowStatus.  # noqa: E501


        :return: The workflow_id of this WorkflowStatus.  # noqa: E501
        :rtype: str
        """
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        """Sets the workflow_id of this WorkflowStatus.


        :param workflow_id: The workflow_id of this WorkflowStatus.  # noqa: E501
        :type: str
        """

        self._workflow_id = workflow_id

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
        if issubclass(WorkflowStatus, dict):
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
        if not isinstance(other, WorkflowStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
