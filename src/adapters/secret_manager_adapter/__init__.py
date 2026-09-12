from boto3.session import Session
from botocore.exceptions import ClientError
from mypy_boto3_secretsmanager.client import SecretsManagerClient

from .port import SecretsManagerPort


class SecretsManagerAdapter(SecretsManagerPort):
    _client: SecretsManagerClient

    def __init__(self):
        self._client = Session().client("secretsmanager")  # type: ignore

    def get_secret(self, secret_name: str) -> str | None:
        try:
            return self._client.get_secret_value(SecretId=secret_name)["SecretString"]
        except ClientError:
            return None

    def store_secret(self, secret_name: str, value: str) -> None:
        self._client.put_secret_value(SecretId=secret_name, SecretString=value)
