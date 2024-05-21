from typing import Dict

from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.env_variable_client import EnvVariableClient


class OrkesEnvVariableClient(OrkesBaseClient, EnvVariableClient):
    def __init__(self, configuration: Configuration):
        super().__init__(configuration)

    def save_env_variable(self, name: str, value: str):
        self.environmentResourceApi.create_or_update_env_variable(value, name)

    def get_env_variable(self, name: str) -> str:
        return self.environmentResourceApi.get1(name)

    def get_all_env_variables(self) -> Dict:
        return self.environmentResourceApi.get_all()

    def delete_env_variable(self, name: str):
        self.environmentResourceApi.delete_env_variable(name)