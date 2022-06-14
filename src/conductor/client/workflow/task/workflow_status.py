from enum import Enum


class WorkflowStatus(str, Enum):
    CompletedWorkflow = "COMPLETED",
    FailedWorkflow = "FAILED",
    PausedWorkflow = "PAUSED",
    RunningWorkflow = "RUNNING",
    TerminatedWorkflow = "TERMINATED",
    TimedOutWorkflow = "TIMED_OUT",
