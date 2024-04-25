from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_iss: str = "mg"
