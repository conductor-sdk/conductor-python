import pprint
import re  # noqa: F401

import six


class WorkflowScheduleExecutionModel(object):
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
        "execution_id": "str",
        "schedule_name": "str",
        "scheduled_time": "int",
        "execution_time": "int",
        "workflow_name": "str",
        "workflow_id": "str",
        "reason": "str",
        "stack_trace": "str",
        "start_workflow_request": "StartWorkflowRequest",
        "state": "str",
    }

    attribute_map = {
        "execution_id": "executionId",
        "schedule_name": "scheduleName",
        "scheduled_time": "scheduledTime",
        "execution_time": "executionTime",
        "workflow_name": "workflowName",
        "workflow_id": "workflowId",
        "reason": "reason",
        "stack_trace": "stackTrace",
        "start_workflow_request": "startWorkflowRequest",
        "state": "state",
    }

    def __init__(
        self,
        execution_id=None,
        schedule_name=None,
        scheduled_time=None,
        execution_time=None,
        workflow_name=None,
        workflow_id=None,
        reason=None,
        stack_trace=None,
        start_workflow_request=None,
        state=None,
    ):  # noqa: E501
        """WorkflowScheduleExecutionModel - a model defined in Swagger"""  # noqa: E501
        self._execution_id = None
        self._schedule_name = None
        self._scheduled_time = None
        self._execution_time = None
        self._workflow_name = None
        self._workflow_id = None
        self._reason = None
        self._stack_trace = None
        self._start_workflow_request = None
        self._state = None
        self.discriminator = None
        if execution_id is not None:
            self.execution_id = execution_id
        if schedule_name is not None:
            self.schedule_name = schedule_name
        if scheduled_time is not None:
            self.scheduled_time = scheduled_time
        if execution_time is not None:
            self.execution_time = execution_time
        if workflow_name is not None:
            self.workflow_name = workflow_name
        if workflow_id is not None:
            self.workflow_id = workflow_id
        if reason is not None:
            self.reason = reason
        if stack_trace is not None:
            self.stack_trace = stack_trace
        if start_workflow_request is not None:
            self.start_workflow_request = start_workflow_request
        if state is not None:
            self.state = state

    @property
    def execution_id(self):
        """Gets the execution_id of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The execution_id of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this WorkflowScheduleExecutionModel.


        :param execution_id: The execution_id of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: str
        """

        self._execution_id = execution_id

    @property
    def schedule_name(self):
        """Gets the schedule_name of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The schedule_name of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: str
        """
        return self._schedule_name

    @schedule_name.setter
    def schedule_name(self, schedule_name):
        """Sets the schedule_name of this WorkflowScheduleExecutionModel.


        :param schedule_name: The schedule_name of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: str
        """

        self._schedule_name = schedule_name

    @property
    def scheduled_time(self):
        """Gets the scheduled_time of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The scheduled_time of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: int
        """
        return self._scheduled_time

    @scheduled_time.setter
    def scheduled_time(self, scheduled_time):
        """Sets the scheduled_time of this WorkflowScheduleExecutionModel.


        :param scheduled_time: The scheduled_time of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: int
        """

        self._scheduled_time = scheduled_time

    @property
    def execution_time(self):
        """Gets the execution_time of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The execution_time of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: int
        """
        return self._execution_time

    @execution_time.setter
    def execution_time(self, execution_time):
        """Sets the execution_time of this WorkflowScheduleExecutionModel.


        :param execution_time: The execution_time of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: int
        """

        self._execution_time = execution_time

    @property
    def workflow_name(self):
        """Gets the workflow_name of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The workflow_name of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: str
        """
        return self._workflow_name

    @workflow_name.setter
    def workflow_name(self, workflow_name):
        """Sets the workflow_name of this WorkflowScheduleExecutionModel.


        :param workflow_name: The workflow_name of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: str
        """

        self._workflow_name = workflow_name

    @property
    def workflow_id(self):
        """Gets the workflow_id of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The workflow_id of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: str
        """
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        """Sets the workflow_id of this WorkflowScheduleExecutionModel.


        :param workflow_id: The workflow_id of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: str
        """

        self._workflow_id = workflow_id

    @property
    def reason(self):
        """Gets the reason of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The reason of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this WorkflowScheduleExecutionModel.


        :param reason: The reason of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: str
        """

        self._reason = reason

    @property
    def stack_trace(self):
        """Gets the stack_trace of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The stack_trace of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: str
        """
        return self._stack_trace

    @stack_trace.setter
    def stack_trace(self, stack_trace):
        """Sets the stack_trace of this WorkflowScheduleExecutionModel.


        :param stack_trace: The stack_trace of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: str
        """

        self._stack_trace = stack_trace

    @property
    def start_workflow_request(self):
        """Gets the start_workflow_request of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The start_workflow_request of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: StartWorkflowRequest
        """
        return self._start_workflow_request

    @start_workflow_request.setter
    def start_workflow_request(self, start_workflow_request):
        """Sets the start_workflow_request of this WorkflowScheduleExecutionModel.


        :param start_workflow_request: The start_workflow_request of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: StartWorkflowRequest
        """

        self._start_workflow_request = start_workflow_request

    @property
    def state(self):
        """Gets the state of this WorkflowScheduleExecutionModel.  # noqa: E501


        :return: The state of this WorkflowScheduleExecutionModel.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this WorkflowScheduleExecutionModel.


        :param state: The state of this WorkflowScheduleExecutionModel.  # noqa: E501
        :type: str
        """
        allowed_values = ["POLLED", "FAILED", "EXECUTED"]  # noqa: E501
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}".format(  # noqa: E501
                    state, allowed_values
                )
            )

        self._state = state

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(WorkflowScheduleExecutionModel, dict):
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
        if not isinstance(other, WorkflowScheduleExecutionModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
