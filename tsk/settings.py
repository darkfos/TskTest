from dotenv import load_dotenv
from os import getenv
from pathlib import Path

#url_project = Path(__file__).parent


load_dotenv()


class Settings:

    DB_URL: str = getenv("DATABASE_URL")
    ECHO_DB: bool = True


settings = Settings()