from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List
from enum import Enum
from .signal_response import SignalResponse


class TaskStatus(Enum):
    """Enum for task status"""
    IN_PROGRESS = "IN_PROGRESS"
    CANCELED = "CANCELED"
    FAILED = "FAILED"
    FAILED_WITH_TERMINAL_ERROR = "FAILED_WITH_TERMINAL_ERROR"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"
    SCHEDULED = "SCHEDULED"
    TIMED_OUT = "TIMED_OUT"
    READY_FOR_RERUN = "READY_FOR_RERUN"
    SKIPPED = "SKIPPED"


@dataclass
class TaskRun(SignalResponse):
    """Task run model extending SignalResponse"""

    task_type: Optional[str] = None
    task_id: Optional[str] = None
    reference_task_name: Optional[str] = None
    retry_count: int = 0
    task_def_name: Optional[str] = None
    retried_task_id: Optional[str] = None
    workflow_type: Optional[str] = None
    reason_for_incompletion: Optional[str] = None
    priority: int = 0
    variables: Optional[Dict[str, Any]] = None
    tasks: Optional[List[Any]] = None  # List of Task objects
    created_by: Optional[str] = None
    create_time: int = 0
    update_time: int = 0
    status: Optional[TaskStatus] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON serialization"""
        data = asdict(self)
        camel_case_data = super().to_dict()

        field_mapping = {
            'task_type': 'taskType',
            'task_id': 'taskId',
            'reference_task_name': 'referenceTaskName',
            'retry_count': 'retryCount',
            'task_def_name': 'taskDefName',
            'retried_task_id': 'retriedTaskId',
            'workflow_type': 'workflowType',
            'reason_for_incompletion': 'reasonForIncompletion',
            'priority': 'priority',
            'variables': 'variables',
            'tasks': 'tasks',
            'created_by': 'createdBy',
            'create_time': 'createTime',
            'update_time': 'updateTime',
            'status': 'status'
        }

        for snake_key, camel_key in field_mapping.items():
            if snake_key in data and data[snake_key] is not None:
                if isinstance(data[snake_key], TaskStatus):
                    camel_case_data[camel_key] = data[snake_key].value
                else:
                    camel_case_data[camel_key] = data[snake_key]

        return camel_case_data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskRun':
        """Create instance from dictionary with camelCase keys"""
        snake_case_data = {}

        # Handle parent class fields
        parent_mapping = {
            'responseType': 'response_type',
            'targetWorkflowId': 'target_workflow_id',
            'targetWorkflowStatus': 'target_workflow_status',
            'requestId': 'request_id',
            'workflowId': 'workflow_id',
            'correlationId': 'correlation_id',
            'input': 'input',
            'output': 'output'
        }

        field_mapping = {
            'taskType': 'task_type',
            'taskId': 'task_id',
            'referenceTaskName': 'reference_task_name',
            'retryCount': 'retry_count',
            'taskDefName': 'task_def_name',
            'retriedTaskId': 'retried_task_id',
            'workflowType': 'workflow_type',
            'reasonForIncompletion': 'reason_for_incompletion',
            'priority': 'priority',
            'variables': 'variables',
            'tasks': 'tasks',
            'createdBy': 'created_by',
            'createTime': 'create_time',
            'updateTime': 'update_time',
            'status': 'status'
        }

        all_mappings = {**parent_mapping, **field_mapping}

        for camel_key, snake_key in all_mappings.items():
            if camel_key in data:
                if snake_key == 'status' and data[camel_key]:
                    snake_case_data[snake_key] = TaskStatus(data[camel_key])
                else:
                    snake_case_data[snake_key] = data[camel_key]

        return cls(**snake_case_data)