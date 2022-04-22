class HttpSettings:
    def __init__(self, base_url='.', headers={}, external_storage_settings=None):
        self.base_url = base_url
        self.headers = headers
        self.external_storage_settings = external_storage_settings
