from tsk.db.mainbase import MainBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List
from typing import Literal


class UserTable(MainBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String(150))
    login: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    sex: Mapped[Literal["male", "female"]] = mapped_column(String(12))
    password: Mapped[int] = mapped_column(Integer, nullable=False)

    #For detail
    posts: Mapped[List["PostTable"]] = relationship(back_populates="user")

    def __str__(self):
        return str({
            data: value for data, value in self.__dict__.items() if data not in ("id")
        })

    def __repr__(self):
        return self.__str__()