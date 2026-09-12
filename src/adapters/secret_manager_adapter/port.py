from abc import ABC, abstractmethod


class SecretsManagerPort(ABC):
    @abstractmethod
    def get_secret(self, secret_name: str) -> str | None:
        pass

    @abstractmethod
    def store_secret(self, secret_name: str, value: str) -> None:
        pass
