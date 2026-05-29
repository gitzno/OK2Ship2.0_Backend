from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "1433"
    DB_NAME: str = "OK2SHIP_SMT"
    DB_USER: str = "sa"
    DB_PASSWORD: str = "YourStrong(!)Password"

    # Cấu hình bảo mật JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # Cấu hình để Pydantic tự động quét file .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()