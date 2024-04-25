from pydantic import BaseModel


class LoginResponse(BaseModel):
    bearer_token: str
