from aws_lambda_powertools.utilities.typing import LambdaContext

from main import init_and_sync


def lambda_handler(event: dict[str, str], _: LambdaContext) -> str:
    return init_and_sync().to_json()  # type: ignore
