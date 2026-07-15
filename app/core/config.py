from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    UPLOAD_DIR: str = "uploads"
    EXTRACTED_TEXT_DIR: str = "extracted_text"
    MAX_FILE_SIZE: int = 10* 1024* 1024
    ALLOWED_FILE_TYPES: list[str] = ["application/pdf"]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()    