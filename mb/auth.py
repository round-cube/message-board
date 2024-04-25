from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Request
from typing import Annotated
from jwt import decode


security = HTTPBearer()


def get_payload(token: str, secret_key: str, algorithms: list[str]) -> dict:
    """Decode the payload from a JWT token."""
    return decode(token, secret_key, algorithms=algorithms)


def get_user_id(
    request: Request, token: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """Check the bearer token and return corresponding user ID."""
    payload = get_payload(
        token.credentials,
        request.app.settings.secret_key,
        algorithms=[request.app.settings.jwt_algorithm],
    )
    return payload["sub"]
