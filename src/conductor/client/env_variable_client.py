from abc import ABC, abstractmethod
from typing import Dict


class EnvVariableClient(ABC):
    @abstractmethod
    def save_env_variable(self, name: str, value: str):
        pass

    @abstractmethod
    def get_env_variable(self, name: str) -> str:
        pass

    @abstractmethod
    def get_all_env_variables(self) -> Dict:
        pass

    @abstractmethod
    def delete_env_variable(self, name: str):
        pass
