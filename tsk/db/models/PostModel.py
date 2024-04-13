from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from tsk.db.mainbase import MainBase
from tsk.settings import SettingsPost


class PostTable(MainBase):
    __tablename__ = "Post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(SettingsPost.title_length), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    #For detail
    user: Mapped["UserTable"] = relationship(back_populates="posts")