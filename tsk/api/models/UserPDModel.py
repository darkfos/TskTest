from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated, Optional


class SexUser(str, Enum):

    male: str = "male"
    female: str = "female"


class AddNewUser(BaseModel):
    """
    Model for add a new user
    """

    name_user: Annotated[str, Field(max_length=150)]
    login: Annotated[str, Field(max_length=80, min_length=6)]
    sex: SexUser
    hashed_password: Annotated[str,  Field(min_length=6)]


class InformationAboutUser(BaseModel):
    name_user: Annotated[str, Field(max_length=150)]
    sex: SexUser


class UserUpdate(BaseModel):
    name_user: Annotated[Optional[str], Field(default=..., max_length=150)] = None
    sex: Annotated[Optional[SexUser], Field(default=...)] = None

class User(AddNewUser, BaseModel):
    """
    Basic model user
    """

    id: Annotated[int, Field()]


class UserRequest(BaseModel):

    login: Annotated[str, Field(max_length=80, min_length=6)]
    hashed_password: Annotated[str, Field(min_length=6)]


class Token(BaseModel):
    access_token: str
    token_type: str