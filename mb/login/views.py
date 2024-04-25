import jwt
from fastapi import APIRouter
from starlette.requests import Request

from mb.login.validation import LoginResponse

router = APIRouter()


@router.post("/login")
async def login(request: Request) -> LoginResponse:
    """Login and get a bearer token."""
    jwt_payload = {
        "iss": request.app.settings.jwt_iss,
        "sub": request.app.storage.generate_id("usr"),
    }
    return LoginResponse(
        bearer_token=jwt.encode(
            jwt_payload,
            request.app.settings.secret_key,
            algorithm=request.app.settings.jwt_algorithm,
        )
    )
