class MetricsSettings:
    def __init__(self, directory='.', file_name='metrics.log', update_interval=0.1):
        self.directory = directory
        self.file_name = file_name
        self.update_interval = update_interval
