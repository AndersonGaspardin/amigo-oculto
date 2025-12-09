import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from typing import ClassVar

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL:ClassVar[str] = os.getenv("DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
templates = Jinja2Templates(directory="app/templates")
