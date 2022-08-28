from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from tests.unit.resources.workers import ClassWorker
import pytest


TASK_ID = 'VALID_TASK_ID'
WORKFLOW_INSTANCE_ID = 'VALID_WORKFLOW_INSTANCE_ID'
UPDATE_TASK_RESPONSE = 'VALID_UPDATE_TASK_RESPONSE'


def test_initialization_without_configuration():
    TaskRunner(
        configuration=None,
        worker=_get_valid_worker()
    )


def test_initialization_with_invalid_worker():
    with pytest.raises(Exception, match='Invalid worker'):
        TaskRunner(
            configuration=Configuration("http://localhost:8080/api"),
            worker=None
        )


def _get_valid_worker():
    return ClassWorker('task')
