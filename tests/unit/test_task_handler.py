from conductor.client.automator.task_handler import TaskHandler
from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from tests.unit.resources.workers import ClassWorker
import pytest


def test_initialization_with_invalid_workers():
    with pytest.raises(TypeError):
        TaskHandler(
            configuration=Configuration(),
            workers=ClassWorker()
        )
