from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # API security configuration
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # API Keys
    API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()