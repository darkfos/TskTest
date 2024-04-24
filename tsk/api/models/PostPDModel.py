from pydantic import BaseModel, Field
from typing import Annotated
from settings import settings_for_post
from datetime import datetime


class Post(BaseModel):
    title: Annotated[str, Field(max_length=settings_for_post.title, min_length=1)]
    description: Annotated[str, Field(min_length=0)]
    date_create: Annotated[datetime, Field(default=settings_for_post.date)]
    user_id: int


class AddPost(BaseModel):
    title: Annotated[str, Field(max_length=settings_for_post.title, min_length=1)]
    description: Annotated[str, Field(min_length=0)]
    date_create: Annotated[datetime, Field(default=settings_for_post.date)] = None


class UpdatePost(AddPost, BaseModel):
    pass


class GetPost(BaseModel):
    title: Annotated[str, Field(max_length=settings_for_post.title, min_length=1)]
    description: Annotated[str, Field(min_length=0)]
    date_create: datetime