from enum import Enum


class TaskResultStatus(str, Enum):
    COMPLETED = "COMPLETED",
    FAILED = "FAILED",
    FAILED_WITH_TERMINAL_ERROR = "FAILED_WITH_TERMINAL_ERROR",
    IN_PROGRESS = "IN_PROGRESS"
