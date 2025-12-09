from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
templates = Jinja2Templates(directory="app/templates")  