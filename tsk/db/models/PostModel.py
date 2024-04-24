import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from db.mainbase import MainBase
from settings import settings_for_post
from datetime import datetime


class PostTable(MainBase):
    __tablename__ = "post"

    title: Mapped[str] = mapped_column(String(settings_for_post.title), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    date_create: Mapped[datetime] = settings_for_post.date
    date_update: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    #For detail
    user: Mapped["UserTable"] = relationship(back_populates="posts")

    def __str__(self):
        return str({
            data: value for data, value in self.__dict__.items() if data not in ("id")
        })

    def __repr__(self):
        return self.__str__()