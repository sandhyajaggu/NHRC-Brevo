from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    GEMINI_API_KEY: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    EMAIL_USER: str
    EMAIL_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    
    BREVO_API_KEY : str
    BREVO_SENDER_NAME:str
    BREVO_SENDER_EMAIL:str


    class Config:
        env_file = ".env"
        case_sensitive = True

#  Create settings instance
settings = Settings()

print("BREVO_API_KEY:", settings.BREVO_API_KEY)
print("BREVO_SENDER_NAME:", settings.BREVO_SENDER_NAME)
print("BREVO_SENDER_EMAIL:", settings.BREVO_SENDER_EMAIL)