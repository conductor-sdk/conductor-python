from enum import Enum


class MetricExternalStoragePayloadType(str, Enum):
    TASK_INPUT = "TASK_INPUT"
    TASK_OUTPUT = "TASK_OUTPUT"
