import os
from pathlib import Path
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    ROOT_PATH: str = str(Path(__file__).parent)
    TEMPLATES_PATH: str = os.path.join(ROOT_PATH, "templates")
    STATIC_PATH: str = os.path.join(ROOT_PATH, "static")
    HOST: str
    PORT: int
    DEBUG: bool = True


class BackendSettings(BaseSettings):
    REST_URL: str = "http://127.0.0.1:8888"


class Settings(BackendSettings, AppSettings):
    pass
