from aws_lambda_powertools.utilities.typing import LambdaContext

from main import sync


def lambda_handler(event: dict[str, str], _: LambdaContext) -> str:
    return sync().to_json()  # type: ignore
