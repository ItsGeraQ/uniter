from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool
    MONGO_URI: str
    COGNITO_REGION: str
    COGNITO_USERPOOL_ID: str
    COGNITO_CLIENT_ID: str
    COGNITO_CLIENT_SECRET: str
    OPENAI_API_KEY: str
    SECRET_KEY : str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

    