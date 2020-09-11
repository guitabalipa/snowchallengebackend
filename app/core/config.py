import secrets

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    EMAIL_TEST_USER: str = "test@example.com"
    PASSWORD_TEST_USER: str = "123qwe"

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    PROJECT_NAME: str

    AWS_PRE_SIGNED_URL_EXPIRE_MINUTES: int = 60 * 24
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_IMAGE_BUCKET: str

    DATABASE_URL: str


load_dotenv()
settings = Settings()
