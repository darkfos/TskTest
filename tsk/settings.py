import datetime

from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from typing import Final

#url_project = Path(__file__).parent


load_dotenv()


class Settings:

    __DB_URL: Final[str] = getenv("DATABASE_URL")
    __ECHO_DB: Final[bool] = True
    __AUTH_KEY: Final[str] = getenv("SECRET_KEY_TO_AUTH")
    __AUTH_KEY_REFRESH: Final[str] = getenv("SECRET_KEY_FOR_REFRESH_TOKEN")

    @property
    def db_url(self) -> str:
        return self.__DB_URL

    @property
    def echo_db(self) -> bool:
        return self.__ECHO_DB

    @echo_db.setter
    def echo_db(self, echo: bool) -> None:
        self.__ECHO_DB = echo

    @property
    def get_auth_key(self) -> str: return self.__AUTH_KEY

    @property
    def get_refresh_key(self) -> str: return self.__AUTH_KEY_REFRESH
class SettingsPost:
    __title_length: Final[int] = 150
    __date: Final[datetime.datetime] = datetime.datetime.now().date()

    @property
    def title(self) -> int:
        return self.__title_length

    @title.setter
    def title(self, new_title: int) -> None:
        self.__title_length = new_title

    @property
    def date(self) -> datetime.datetime:
        return self.__date

    @date.setter
    def date(self, new_date: datetime):
        if type(new_date) is datetime.date:
            self.__date = new_date
        else:
            raise ValueError("Не соответствие типов")


settings = Settings()
settings_for_post = SettingsPost()