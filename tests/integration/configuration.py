import os

from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings


def get_configuration():
    configuration = Configuration()
    configuration.debug = False
    configuration.apply_logging_config()

    return configuration
