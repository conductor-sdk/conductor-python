import pprint
import re  # noqa: F401
import six
from dataclasses import dataclass, field, fields
from typing import Dict, List, Optional, Any, Union
from deprecated import deprecated

from conductor.client.http.models import WorkflowTask
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus


@dataclass
class Task:
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
    _task_type: str = field(default=None)
    _status: str = field(default=None)
    _input_data: Dict[str, object] = field(default=None)
    _reference_task_name: str = field(default=None)
    _retry_count: int = field(default=None)
    _seq: int = field(default=None)
    _correlation_id: str = field(default=None)
    _poll_count: int = field(default=None)
    _task_def_name: str = field(default=None)
    _scheduled_time: int = field(default=None)
    _start_time: int = field(default=None)
    _end_time: int = field(default=None)
    _update_time: int = field(default=None)
    _start_delay_in_seconds: int = field(default=None)
    _retried_task_id: str = field(default=None)
    _retried: bool = field(default=None)
    _executed: bool = field(default=None)
    _callback_from_worker: bool = field(default=None)
    _response_timeout_seconds: int = field(default=None)
    _workflow_instance_id: str = field(default=None)
    _workflow_type: str = field(default=None)
    _task_id: str = field(default=None)
    _reason_for_incompletion: str = field(default=None)
    _callback_after_seconds: int = field(default=None)
    _worker_id: str = field(default=None)
    _output_data: Dict[str, object] = field(default=None)
    _workflow_task: WorkflowTask = field(default=None)
    _domain: str = field(default=None)
    _rate_limit_per_frequency: int = field(default=None)
    _rate_limit_frequency_in_seconds: int = field(default=None)
    _external_input_payload_storage_path: str = field(default=None)
    _external_output_payload_storage_path: str = field(default=None)
    _workflow_priority: int = field(default=None)
    _execution_name_space: str = field(default=None)
    _isolation_group_id: str = field(default=None)
    _iteration: int = field(default=None)
    _sub_workflow_id: str = field(default=None)
    _subworkflow_changed: bool = field(default=None)
    _parent_task_id: str = field(default=None)
    _first_start_time: int = field(default=None)
    
    # Fields that are in Python but not in Java
    _loop_over_task: bool = field(default=None)
    _task_definition: Any = field(default=None)
    _queue_wait_time: int = field(default=None)
    
    swagger_types = {
        'task_type': 'str',
        'status': 'str',
        'input_data': 'dict(str, object)',
        'reference_task_name': 'str',
        'retry_count': 'int',
        'seq': 'int',
        'correlation_id': 'str',
        'poll_count': 'int',
        'task_def_name': 'str',
        'scheduled_time': 'int',
        'start_time': 'int',
        'end_time': 'int',
        'update_time': 'int',
        'start_delay_in_seconds': 'int',
        'retried_task_id': 'str',
        'retried': 'bool',
        'executed': 'bool',
        'callback_from_worker': 'bool',
        'response_timeout_seconds': 'int',
        'workflow_instance_id': 'str',
        'workflow_type': 'str',
        'task_id': 'str',
        'reason_for_incompletion': 'str',
        'callback_after_seconds': 'int',
        'worker_id': 'str',
        'output_data': 'dict(str, object)',
        'workflow_task': 'WorkflowTask',
        'domain': 'str',
        'rate_limit_per_frequency': 'int',
        'rate_limit_frequency_in_seconds': 'int',
        'external_input_payload_storage_path': 'str',
        'external_output_payload_storage_path': 'str',
        'workflow_priority': 'int',
        'execution_name_space': 'str',
        'isolation_group_id': 'str',
        'iteration': 'int',
        'sub_workflow_id': 'str',
        'subworkflow_changed': 'bool',
        'parent_task_id': 'str',
        'first_start_time': 'int',
        'loop_over_task': 'bool',
        'task_definition': 'TaskDef',
        'queue_wait_time': 'int'
    }

    attribute_map = {
        'task_type': 'taskType',
        'status': 'status',
        'input_data': 'inputData',
        'reference_task_name': 'referenceTaskName',
        'retry_count': 'retryCount',
        'seq': 'seq',
        'correlation_id': 'correlationId',
        'poll_count': 'pollCount',
        'task_def_name': 'taskDefName',
        'scheduled_time': 'scheduledTime',
        'start_time': 'startTime',
        'end_time': 'endTime',
        'update_time': 'updateTime',
        'start_delay_in_seconds': 'startDelayInSeconds',
        'retried_task_id': 'retriedTaskId',
        'retried': 'retried',
        'executed': 'executed',
        'callback_from_worker': 'callbackFromWorker',
        'response_timeout_seconds': 'responseTimeoutSeconds',
        'workflow_instance_id': 'workflowInstanceId',
        'workflow_type': 'workflowType',
        'task_id': 'taskId',
        'reason_for_incompletion': 'reasonForIncompletion',
        'callback_after_seconds': 'callbackAfterSeconds',
        'worker_id': 'workerId',
        'output_data': 'outputData',
        'workflow_task': 'workflowTask',
        'domain': 'domain',
        'rate_limit_per_frequency': 'rateLimitPerFrequency',
        'rate_limit_frequency_in_seconds': 'rateLimitFrequencyInSeconds',
        'external_input_payload_storage_path': 'externalInputPayloadStoragePath',
        'external_output_payload_storage_path': 'externalOutputPayloadStoragePath',
        'workflow_priority': 'workflowPriority',
        'execution_name_space': 'executionNameSpace',
        'isolation_group_id': 'isolationGroupId',
        'iteration': 'iteration',
        'sub_workflow_id': 'subWorkflowId',
        'subworkflow_changed': 'subworkflowChanged',
        'parent_task_id': 'parentTaskId',
        'first_start_time': 'firstStartTime',
        'loop_over_task': 'loopOverTask',
        'task_definition': 'taskDefinition',
        'queue_wait_time': 'queueWaitTime'
    }

    def __init__(self, task_type=None, status=None, input_data=None, reference_task_name=None, retry_count=None,
                 seq=None, correlation_id=None, poll_count=None, task_def_name=None, scheduled_time=None,
                 start_time=None, end_time=None, update_time=None, start_delay_in_seconds=None, retried_task_id=None,
                 retried=None, executed=None, callback_from_worker=None, response_timeout_seconds=None,
                 workflow_instance_id=None, workflow_type=None, task_id=None, reason_for_incompletion=None,
                 callback_after_seconds=None, worker_id=None, output_data=None, workflow_task=None, domain=None,
                 rate_limit_per_frequency=None, rate_limit_frequency_in_seconds=None,
                 external_input_payload_storage_path=None, external_output_payload_storage_path=None,
                 workflow_priority=None, execution_name_space=None, isolation_group_id=None, iteration=None,
                 sub_workflow_id=None, subworkflow_changed=None, loop_over_task=None, task_definition=None,
                 queue_wait_time=None, parent_task_id=None, first_start_time=None):  # noqa: E501
        """Task - a model defined in Swagger"""  # noqa: E501
        self._task_type = None
        self._status = None
        self._input_data = None
        self._reference_task_name = None
        self._retry_count = None
        self._seq = None
        self._correlation_id = None
        self._poll_count = None
        self._task_def_name = None
        self._scheduled_time = None
        self._start_time = None
        self._end_time = None
        self._update_time = None
        self._start_delay_in_seconds = None
        self._retried_task_id = None
        self._retried = None
        self._executed = None
        self._callback_from_worker = None
        self._response_timeout_seconds = None
        self._workflow_instance_id = None
        self._workflow_type = None
        self._task_id = None
        self._reason_for_incompletion = None
        self._callback_after_seconds = None
        self._worker_id = None
        self._output_data = None
        self._workflow_task = None
        self._domain = None
        self._rate_limit_per_frequency = None
        self._rate_limit_frequency_in_seconds = None
        self._external_input_payload_storage_path = None
        self._external_output_payload_storage_path = None
        self._workflow_priority = None
        self._execution_name_space = None
        self._isolation_group_id = None
        self._iteration = None
        self._sub_workflow_id = None
        self._subworkflow_changed = None
        self._parent_task_id = None
        self._first_start_time = None
        self._loop_over_task = None
        self._task_definition = None
        self._queue_wait_time = None
        self.discriminator = None
        if task_type is not None:
            self.task_type = task_type
        if status is not None:
            self.status = status
        if input_data is not None:
            self.input_data = input_data
        if reference_task_name is not None:
            self.reference_task_name = reference_task_name
        if retry_count is not None:
            self.retry_count = retry_count
        if seq is not None:
            self.seq = seq
        if correlation_id is not None:
            self.correlation_id = correlation_id
        if poll_count is not None:
            self.poll_count = poll_count
        if task_def_name is not None:
            self.task_def_name = task_def_name
        if scheduled_time is not None:
            self.scheduled_time = scheduled_time
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if update_time is not None:
            self.update_time = update_time
        if start_delay_in_seconds is not None:
            self.start_delay_in_seconds = start_delay_in_seconds
        if retried_task_id is not None:
            self.retried_task_id = retried_task_id
        if retried is not None:
            self.retried = retried
        if executed is not None:
            self.executed = executed
        if callback_from_worker is not None:
            self.callback_from_worker = callback_from_worker
        if response_timeout_seconds is not None:
            self.response_timeout_seconds = response_timeout_seconds
        if workflow_instance_id is not None:
            self.workflow_instance_id = workflow_instance_id
        if workflow_type is not None:
            self.workflow_type = workflow_type
        if task_id is not None:
            self.task_id = task_id
        if reason_for_incompletion is not None:
            self.reason_for_incompletion = reason_for_incompletion
        if callback_after_seconds is not None:
            self.callback_after_seconds = callback_after_seconds
        if worker_id is not None:
            self.worker_id = worker_id
        if output_data is not None:
            self.output_data = output_data
        if workflow_task is not None:
            self.workflow_task = workflow_task
        if domain is not None:
            self.domain = domain
        if rate_limit_per_frequency is not None:
            self.rate_limit_per_frequency = rate_limit_per_frequency
        if rate_limit_frequency_in_seconds is not None:
            self.rate_limit_frequency_in_seconds = rate_limit_frequency_in_seconds
        if external_input_payload_storage_path is not None:
            self.external_input_payload_storage_path = external_input_payload_storage_path
        if external_output_payload_storage_path is not None:
            self.external_output_payload_storage_path = external_output_payload_storage_path
        if workflow_priority is not None:
            self.workflow_priority = workflow_priority
        if execution_name_space is not None:
            self.execution_name_space = execution_name_space
        if isolation_group_id is not None:
            self.isolation_group_id = isolation_group_id
        if iteration is not None:
            self.iteration = iteration
        if sub_workflow_id is not None:
            self.sub_workflow_id = sub_workflow_id
        if subworkflow_changed is not None:
            self.subworkflow_changed = subworkflow_changed
        if parent_task_id is not None:
            self.parent_task_id = parent_task_id
        if first_start_time is not None:
            self.first_start_time = first_start_time
        if loop_over_task is not None:
            self.loop_over_task = loop_over_task
        if task_definition is not None:
            self.task_definition = task_definition
        if queue_wait_time is not None:
            self.queue_wait_time = queue_wait_time

    def __post_init__(self):
        """Post initialization for dataclass"""
        pass

    @property
    def task_type(self):
        """Gets the task_type of this Task.  # noqa: E501


        :return: The task_type of this Task.  # noqa: E501
        :rtype: str
        """
        return self._task_type

    @task_type.setter
    def task_type(self, task_type):
        """Sets the task_type of this Task.


        :param task_type: The task_type of this Task.  # noqa: E501
        :type: str
        """

        self._task_type = task_type

    @property
    def status(self):
        """Gets the status of this Task.  # noqa: E501


        :return: The status of this Task.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Task.


        :param status: The status of this Task.  # noqa: E501
        :type: str
        """
        allowed_values = ["IN_PROGRESS", "CANCELED", "FAILED", "FAILED_WITH_TERMINAL_ERROR", "COMPLETED",
                          "COMPLETED_WITH_ERRORS", "SCHEDULED", "TIMED_OUT", "SKIPPED"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def input_data(self):
        """Gets the input_data of this Task.  # noqa: E501


        :return: The input_data of this Task.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._input_data

    @input_data.setter
    def input_data(self, input_data):
        """Sets the input_data of this Task.


        :param input_data: The input_data of this Task.  # noqa: E501
        :type: dict(str, object)
        """

        self._input_data = input_data

    @property
    def reference_task_name(self):
        """Gets the reference_task_name of this Task.  # noqa: E501


        :return: The reference_task_name of this Task.  # noqa: E501
        :rtype: str
        """
        return self._reference_task_name

    @reference_task_name.setter
    def reference_task_name(self, reference_task_name):
        """Sets the reference_task_name of this Task.


        :param reference_task_name: The reference_task_name of this Task.  # noqa: E501
        :type: str
        """

        self._reference_task_name = reference_task_name

    @property
    def retry_count(self):
        """Gets the retry_count of this Task.  # noqa: E501


        :return: The retry_count of this Task.  # noqa: E501
        :rtype: int
        """
        return self._retry_count

    @retry_count.setter
    def retry_count(self, retry_count):
        """Sets the retry_count of this Task.


        :param retry_count: The retry_count of this Task.  # noqa: E501
        :type: int
        """

        self._retry_count = retry_count

    @property
    def seq(self):
        """Gets the seq of this Task.  # noqa: E501


        :return: The seq of this Task.  # noqa: E501
        :rtype: int
        """
        return self._seq

    @seq.setter
    def seq(self, seq):
        """Sets the seq of this Task.


        :param seq: The seq of this Task.  # noqa: E501
        :type: int
        """

        self._seq = seq

    @property
    def correlation_id(self):
        """Gets the correlation_id of this Task.  # noqa: E501


        :return: The correlation_id of this Task.  # noqa: E501
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """Sets the correlation_id of this Task.


        :param correlation_id: The correlation_id of this Task.  # noqa: E501
        :type: str
        """

        self._correlation_id = correlation_id

    @property
    def poll_count(self):
        """Gets the poll_count of this Task.  # noqa: E501


        :return: The poll_count of this Task.  # noqa: E501
        :rtype: int
        """
        return self._poll_count

    @poll_count.setter
    def poll_count(self, poll_count):
        """Sets the poll_count of this Task.


        :param poll_count: The poll_count of this Task.  # noqa: E501
        :type: int
        """

        self._poll_count = poll_count

    @property
    def task_def_name(self):
        """Gets the task_def_name of this Task.  # noqa: E501


        :return: The task_def_name of this Task.  # noqa: E501
        :rtype: str
        """
        return self._task_def_name

    @task_def_name.setter
    def task_def_name(self, task_def_name):
        """Sets the task_def_name of this Task.


        :param task_def_name: The task_def_name of this Task.  # noqa: E501
        :type: str
        """

        self._task_def_name = task_def_name

    @property
    def scheduled_time(self):
        """Gets the scheduled_time of this Task.  # noqa: E501


        :return: The scheduled_time of this Task.  # noqa: E501
        :rtype: int
        """
        return self._scheduled_time

    @scheduled_time.setter
    def scheduled_time(self, scheduled_time):
        """Sets the scheduled_time of this Task.


        :param scheduled_time: The scheduled_time of this Task.  # noqa: E501
        :type: int
        """

        self._scheduled_time = scheduled_time

    @property
    def start_time(self):
        """Gets the start_time of this Task.  # noqa: E501


        :return: The start_time of this Task.  # noqa: E501
        :rtype: int
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this Task.


        :param start_time: The start_time of this Task.  # noqa: E501
        :type: int
        """

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this Task.  # noqa: E501


        :return: The end_time of this Task.  # noqa: E501
        :rtype: int
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this Task.


        :param end_time: The end_time of this Task.  # noqa: E501
        :type: int
        """

        self._end_time = end_time

    @property
    def update_time(self):
        """Gets the update_time of this Task.  # noqa: E501


        :return: The update_time of this Task.  # noqa: E501
        :rtype: int
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this Task.


        :param update_time: The update_time of this Task.  # noqa: E501
        :type: int
        """

        self._update_time = update_time

    @property
    def start_delay_in_seconds(self):
        """Gets the start_delay_in_seconds of this Task.  # noqa: E501


        :return: The start_delay_in_seconds of this Task.  # noqa: E501
        :rtype: int
        """
        return self._start_delay_in_seconds

    @start_delay_in_seconds.setter
    def start_delay_in_seconds(self, start_delay_in_seconds):
        """Sets the start_delay_in_seconds of this Task.


        :param start_delay_in_seconds: The start_delay_in_seconds of this Task.  # noqa: E501
        :type: int
        """

        self._start_delay_in_seconds = start_delay_in_seconds

    @property
    def retried_task_id(self):
        """Gets the retried_task_id of this Task.  # noqa: E501


        :return: The retried_task_id of this Task.  # noqa: E501
        :rtype: str
        """
        return self._retried_task_id

    @retried_task_id.setter
    def retried_task_id(self, retried_task_id):
        """Sets the retried_task_id of this Task.


        :param retried_task_id: The retried_task_id of this Task.  # noqa: E501
        :type: str
        """

        self._retried_task_id = retried_task_id

    @property
    def retried(self):
        """Gets the retried of this Task.  # noqa: E501


        :return: The retried of this Task.  # noqa: E501
        :rtype: bool
        """
        return self._retried

    @retried.setter
    def retried(self, retried):
        """Sets the retried of this Task.


        :param retried: The retried of this Task.  # noqa: E501
        :type: bool
        """

        self._retried = retried

    @property
    def executed(self):
        """Gets the executed of this Task.  # noqa: E501


        :return: The executed of this Task.  # noqa: E501
        :rtype: bool
        """
        return self._executed

    @executed.setter
    def executed(self, executed):
        """Sets the executed of this Task.


        :param executed: The executed of this Task.  # noqa: E501
        :type: bool
        """

        self._executed = executed

    @property
    def callback_from_worker(self):
        """Gets the callback_from_worker of this Task.  # noqa: E501


        :return: The callback_from_worker of this Task.  # noqa: E501
        :rtype: bool
        """
        return self._callback_from_worker

    @callback_from_worker.setter
    def callback_from_worker(self, callback_from_worker):
        """Sets the callback_from_worker of this Task.


        :param callback_from_worker: The callback_from_worker of this Task.  # noqa: E501
        :type: bool
        """

        self._callback_from_worker = callback_from_worker

    @property
    def response_timeout_seconds(self):
        """Gets the response_timeout_seconds of this Task.  # noqa: E501


        :return: The response_timeout_seconds of this Task.  # noqa: E501
        :rtype: int
        """
        return self._response_timeout_seconds

    @response_timeout_seconds.setter
    def response_timeout_seconds(self, response_timeout_seconds):
        """Sets the response_timeout_seconds of this Task.


        :param response_timeout_seconds: The response_timeout_seconds of this Task.  # noqa: E501
        :type: int
        """

        self._response_timeout_seconds = response_timeout_seconds

    @property
    def workflow_instance_id(self):
        """Gets the workflow_instance_id of this Task.  # noqa: E501


        :return: The workflow_instance_id of this Task.  # noqa: E501
        :rtype: str
        """
        return self._workflow_instance_id

    @workflow_instance_id.setter
    def workflow_instance_id(self, workflow_instance_id):
        """Sets the workflow_instance_id of this Task.


        :param workflow_instance_id: The workflow_instance_id of this Task.  # noqa: E501
        :type: str
        """

        self._workflow_instance_id = workflow_instance_id

    @property
    def workflow_type(self):
        """Gets the workflow_type of this Task.  # noqa: E501


        :return: The workflow_type of this Task.  # noqa: E501
        :rtype: str
        """
        return self._workflow_type

    @workflow_type.setter
    def workflow_type(self, workflow_type):
        """Sets the workflow_type of this Task.


        :param workflow_type: The workflow_type of this Task.  # noqa: E501
        :type: str
        """

        self._workflow_type = workflow_type

    @property
    def task_id(self):
        """Gets the task_id of this Task.  # noqa: E501


        :return: The task_id of this Task.  # noqa: E501
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this Task.


        :param task_id: The task_id of this Task.  # noqa: E501
        :type: str
        """

        self._task_id = task_id

    @property
    def reason_for_incompletion(self):
        """Gets the reason_for_incompletion of this Task.  # noqa: E501


        :return: The reason_for_incompletion of this Task.  # noqa: E501
        :rtype: str
        """
        return self._reason_for_incompletion

    @reason_for_incompletion.setter
    def reason_for_incompletion(self, reason_for_incompletion):
        """Sets the reason_for_incompletion of this Task.


        :param reason_for_incompletion: The reason_for_incompletion of this Task.  # noqa: E501
        :type: str
        """

        self._reason_for_incompletion = reason_for_incompletion

    @property
    def callback_after_seconds(self):
        """Gets the callback_after_seconds of this Task.  # noqa: E501


        :return: The callback_after_seconds of this Task.  # noqa: E501
        :rtype: int
        """
        return self._callback_after_seconds

    @callback_after_seconds.setter
    def callback_after_seconds(self, callback_after_seconds):
        """Sets the callback_after_seconds of this Task.


        :param callback_after_seconds: The callback_after_seconds of this Task.  # noqa: E501
        :type: int
        """

        self._callback_after_seconds = callback_after_seconds

    @property
    def worker_id(self):
        """Gets the worker_id of this Task.  # noqa: E501


        :return: The worker_id of this Task.  # noqa: E501
        :rtype: str
        """
        return self._worker_id

    @worker_id.setter
    def worker_id(self, worker_id):
        """Sets the worker_id of this Task.


        :param worker_id: The worker_id of this Task.  # noqa: E501
        :type: str
        """

        self._worker_id = worker_id

    @property
    def output_data(self):
        """Gets the output_data of this Task.  # noqa: E501


        :return: The output_data of this Task.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._output_data

    @output_data.setter
    def output_data(self, output_data):
        """Sets the output_data of this Task.


        :param output_data: The output_data of this Task.  # noqa: E501
        :type: dict(str, object)
        """

        self._output_data = output_data

    @property
    def workflow_task(self) -> WorkflowTask:
        """Gets the workflow_task of this Task.  # noqa: E501


        :return: The workflow_task of this Task.  # noqa: E501
        :rtype: WorkflowTask
        """
        return self._workflow_task

    @workflow_task.setter
    def workflow_task(self, workflow_task):
        """Sets the workflow_task of this Task.


        :param workflow_task: The workflow_task of this Task.  # noqa: E501
        :type: WorkflowTask
        """

        self._workflow_task = workflow_task

    @property
    def domain(self):
        """Gets the domain of this Task.  # noqa: E501


        :return: The domain of this Task.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this Task.


        :param domain: The domain of this Task.  # noqa: E501
        :type: str
        """

        self._domain = domain

    @property
    def rate_limit_per_frequency(self):
        """Gets the rate_limit_per_frequency of this Task.  # noqa: E501


        :return: The rate_limit_per_frequency of this Task.  # noqa: E501
        :rtype: int
        """
        return self._rate_limit_per_frequency

    @rate_limit_per_frequency.setter
    def rate_limit_per_frequency(self, rate_limit_per_frequency):
        """Sets the rate_limit_per_frequency of this Task.


        :param rate_limit_per_frequency: The rate_limit_per_frequency of this Task.  # noqa: E501
        :type: int
        """

        self._rate_limit_per_frequency = rate_limit_per_frequency

    @property
    def rate_limit_frequency_in_seconds(self):
        """Gets the rate_limit_frequency_in_seconds of this Task.  # noqa: E501


        :return: The rate_limit_frequency_in_seconds of this Task.  # noqa: E501
        :rtype: int
        """
        return self._rate_limit_frequency_in_seconds

    @rate_limit_frequency_in_seconds.setter
    def rate_limit_frequency_in_seconds(self, rate_limit_frequency_in_seconds):
        """Sets the rate_limit_frequency_in_seconds of this Task.


        :param rate_limit_frequency_in_seconds: The rate_limit_frequency_in_seconds of this Task.  # noqa: E501
        :type: int
        """

        self._rate_limit_frequency_in_seconds = rate_limit_frequency_in_seconds

    @property
    def external_input_payload_storage_path(self):
        """Gets the external_input_payload_storage_path of this Task.  # noqa: E501


        :return: The external_input_payload_storage_path of this Task.  # noqa: E501
        :rtype: str
        """
        return self._external_input_payload_storage_path

    @external_input_payload_storage_path.setter
    def external_input_payload_storage_path(self, external_input_payload_storage_path):
        """Sets the external_input_payload_storage_path of this Task.


        :param external_input_payload_storage_path: The external_input_payload_storage_path of this Task.  # noqa: E501
        :type: str
        """

        self._external_input_payload_storage_path = external_input_payload_storage_path

    @property
    def external_output_payload_storage_path(self):
        """Gets the external_output_payload_storage_path of this Task.  # noqa: E501


        :return: The external_output_payload_storage_path of this Task.  # noqa: E501
        :rtype: str
        """
        return self._external_output_payload_storage_path

    @external_output_payload_storage_path.setter
    def external_output_payload_storage_path(self, external_output_payload_storage_path):
        """Sets the external_output_payload_storage_path of this Task.


        :param external_output_payload_storage_path: The external_output_payload_storage_path of this Task.  # noqa: E501
        :type: str
        """

        self._external_output_payload_storage_path = external_output_payload_storage_path

    @property
    def workflow_priority(self):
        """Gets the workflow_priority of this Task.  # noqa: E501


        :return: The workflow_priority of this Task.  # noqa: E501
        :rtype: int
        """
        return self._workflow_priority

    @workflow_priority.setter
    def workflow_priority(self, workflow_priority):
        """Sets the workflow_priority of this Task.


        :param workflow_priority: The workflow_priority of this Task.  # noqa: E501
        :type: int
        """

        self._workflow_priority = workflow_priority

    @property
    def execution_name_space(self):
        """Gets the execution_name_space of this Task.  # noqa: E501


        :return: The execution_name_space of this Task.  # noqa: E501
        :rtype: str
        """
        return self._execution_name_space

    @execution_name_space.setter
    def execution_name_space(self, execution_name_space):
        """Sets the execution_name_space of this Task.


        :param execution_name_space: The execution_name_space of this Task.  # noqa: E501
        :type: str
        """

        self._execution_name_space = execution_name_space

    @property
    def isolation_group_id(self):
        """Gets the isolation_group_id of this Task.  # noqa: E501


        :return: The isolation_group_id of this Task.  # noqa: E501
        :rtype: str
        """
        return self._isolation_group_id

    @isolation_group_id.setter
    def isolation_group_id(self, isolation_group_id):
        """Sets the isolation_group_id of this Task.


        :param isolation_group_id: The isolation_group_id of this Task.  # noqa: E501
        :type: str
        """

        self._isolation_group_id = isolation_group_id

    @property
    def iteration(self):
        """Gets the iteration of this Task.  # noqa: E501


        :return: The iteration of this Task.  # noqa: E501
        :rtype: int
        """
        return self._iteration

    @iteration.setter
    def iteration(self, iteration):
        """Sets the iteration of this Task.


        :param iteration: The iteration of this Task.  # noqa: E501
        :type: int
        """

        self._iteration = iteration

    @property
    def sub_workflow_id(self):
        """Gets the sub_workflow_id of this Task.  # noqa: E501


        :return: The sub_workflow_id of this Task.  # noqa: E501
        :rtype: str
        """
        return self._sub_workflow_id

    @sub_workflow_id.setter
    def sub_workflow_id(self, sub_workflow_id):
        """Sets the sub_workflow_id of this Task.


        :param sub_workflow_id: The sub_workflow_id of this Task.  # noqa: E501
        :type: str
        """

        self._sub_workflow_id = sub_workflow_id

    @property
    def subworkflow_changed(self):
        """Gets the subworkflow_changed of this Task.  # noqa: E501


        :return: The subworkflow_changed of this Task.  # noqa: E501
        :rtype: bool
        """
        return self._subworkflow_changed

    @subworkflow_changed.setter
    def subworkflow_changed(self, subworkflow_changed):
        """Sets the subworkflow_changed of this Task.


        :param subworkflow_changed: The subworkflow_changed of this Task.  # noqa: E501
        :type: bool
        """

        self._subworkflow_changed = subworkflow_changed

    @property
    def parent_task_id(self):
        return self._parent_task_id

    @parent_task_id.setter
    def parent_task_id(self, parent_task_id):
        self._parent_task_id = parent_task_id

    @property
    def first_start_time(self):
        return self._first_start_time

    @first_start_time.setter
    def first_start_time(self, first_start_time):
        self._first_start_time = first_start_time

    @property
    def loop_over_task(self):
        """Gets the loop_over_task of this Task.  # noqa: E501


        :return: The loop_over_task of this Task.  # noqa: E501
        :rtype: bool
        """
        return self._loop_over_task

    @loop_over_task.setter
    def loop_over_task(self, loop_over_task):
        """Sets the loop_over_task of this Task.


        :param loop_over_task: The loop_over_task of this Task.  # noqa: E501
        :type: bool
        """

        self._loop_over_task = loop_over_task

    @property
    def task_definition(self):
        """Gets the task_definition of this Task.  # noqa: E501


        :return: The task_definition of this Task.  # noqa: E501
        :rtype: TaskDef
        """
        return self._task_definition

    @task_definition.setter
    def task_definition(self, task_definition):
        """Sets the task_definition of this Task.


        :param task_definition: The task_definition of this Task.  # noqa: E501
        :type: TaskDef
        """

        self._task_definition = task_definition

    @property
    def queue_wait_time(self):
        """Gets the queue_wait_time of this Task.  # noqa: E501


        :return: The queue_wait_time of this Task.  # noqa: E501
        :rtype: int
        """
        return self._queue_wait_time

    @queue_wait_time.setter
    def queue_wait_time(self, queue_wait_time):
        """Sets the queue_wait_time of this Task.


        :param queue_wait_time: The queue_wait_time of this Task.  # noqa: E501
        :type: int
        """

        self._queue_wait_time = queue_wait_time

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
        if issubclass(Task, dict):
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
        if not isinstance(other, Task):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    def to_task_result(self, status: TaskResultStatus = TaskResultStatus.COMPLETED) -> TaskResult:
        task_result = TaskResult(
            task_id=self.task_id,
            workflow_instance_id=self.workflow_instance_id,
            worker_id=self.worker_id,
            status=status,
        )
        return task_result