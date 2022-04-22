class ExternalStorageSettings:
    def __init__(
        self,
        task_output_payload_threshold_kb,
        task_output_max_payload_threshold_kb,
        external_storage_handler
    ):
        self.task_output_payload_threshold_kb = task_output_payload_threshold_kb
        self.task_output_max_payload_threshold_kb = task_output_max_payload_threshold_kb
        self.external_storage_handler = external_storage_handler
