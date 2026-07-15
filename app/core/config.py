from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    GEMINI_API_KEY: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    

    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None

    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: str | None = None

    FROM_EMAIL: str | None = None
    FROM_NAME: str = "National Human Resource Club"
    
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