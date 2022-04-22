from enum import Enum


class MetricExternalStorageOperation(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
