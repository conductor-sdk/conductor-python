from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
import logging


class Configuration:
    AUTH_TOKEN = None

    def __init__(
            self,
            base_url: str = "http://localhost:8080",
            debug: bool = False,
            authentication_settings: AuthenticationSettings = None,
            server_api_url: str = None,
    ):
        if server_api_url != None:
            self.host = server_api_url
        else:
            self.host = base_url + '/api/'

        self.temp_folder_path = None

        self.authentication_settings = authentication_settings

        # Debug switch
        self.debug = debug
        # Log format
        self._logger_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        # Apply logging settings
        logging.basicConfig(
            format=self._logger_format,
            level=self.__log_level
        )

        # SSL/TLS verification
        # Set this to false to skip verifying SSL certificate when calling API
        # from https server.
        self.verify_ssl = True
        # Set this to customize the certificate file to verify the peer.
        self.ssl_ca_cert = None
        # client certificate file
        self.cert_file = None
        # client key file
        self.key_file = None

        # Proxy URL
        self.proxy = None
        # Safe chars for path_param
        self.safe_chars_for_path_param = ''

    @property
    def debug(self):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self.__debug

    @debug.setter
    def debug(self, value):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        self.__debug = value
        if self.__debug:
            self.__log_level = logging.DEBUG
        else:
            self.__log_level = logging.INFO

    @property
    def _logger_format(self):
        """The _logger format.

        The _logger_formatter will be updated when sets _logger_format.

        :param value: The format string.
        :type: str
        """
        return self.___logger_format

    @_logger_format.setter
    def _logger_format(self, value):
        """The _logger format.

        The _logger_formatter will be updated when sets _logger_format.

        :param value: The format string.
        :type: str
        """
        self.___logger_format = value

    def update_token(self, token: str) -> None:
        self.AUTH_TOKEN = token
