from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from six.moves import http_client as httplib
import logging
import multiprocessing
import os


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
        self.logger_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

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
        # Set this to True/False to enable/disable SSL hostname verification.
        self.assert_hostname = None

        # urllib3 connection pool's maximum number of connections saved
        # per pool. urllib3 uses 1 connection as default value, but this is
        # not the best value when you are making a lot of possibly parallel
        # requests to the same host, which is often the case here.
        # cpu_count * 5 is used as default value to increase performance.
        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5

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
            # turn on httplib debug
            httplib.HTTPConnection.debuglevel = 1
            self.__log_level = logging.DEBUG
        else:
            # turn off httplib debug
            httplib.HTTPConnection.debuglevel = 0
            self.__log_level = logging.INFO

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self.__logger_format

    @logger_format.setter
    def logger_format(self, value):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        self.__logger_format = value

    def apply_logging_config(self):
        logging.basicConfig(
            format=self.logger_format,
            level=self.__log_level
        )
        logging.getLogger('urllib3').setLevel(logging.WARNING)

    @staticmethod
    def get_logging_formatted_name(name):
        return f'[{os.getpid()}] {name}'

    def update_token(self, token: str) -> None:
        self.AUTH_TOKEN = token
