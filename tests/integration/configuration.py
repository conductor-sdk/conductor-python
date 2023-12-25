import os

from conductor.client.configuration.configuration import Configuration

from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings


def get_configuration():
    required_envs = {
        'KEY': 'KEY',
        'SECRET': 'SECRET',
        'URL': 'CONDUCTOR_SERVER_URL',
    }
    envs = {}
    for key, env in required_envs.items():
        value = os.getenv(env)
        if value is None or value == '':
            print(f'ENV not set - {env}')
        else:
            envs[key] = value
    params = {
        'server_api_url': envs['URL'],
        'debug': True,
    }
    if 'KEY' in envs and 'SECRET' in envs:
        params['authentication_settings'] = AuthenticationSettings(
            key_id=envs['KEY'],
            key_secret=envs['SECRET']
        )
    configuration = Configuration(**params)
    configuration.debug = False
    configuration.apply_logging_config()

    return configuration