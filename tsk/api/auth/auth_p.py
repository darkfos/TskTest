from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from tsk.settings import settings
from tsk.api.models.UserPDModel import UserRequest, Token, AddNewUser
from tsk.api.services.UserService import UserService

from tsk.db.db_connection import db_connect
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

#To authentication user
auth_router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

auth_key = settings.get_auth_key
algorithm = "HS256"


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        session_db: Annotated[AsyncSession, Depends(db_connect.get_session)],
        new_user: AddNewUser) -> dict:

    new_user.password = bcrypt_context.hash(new_user.password)
    result = await UserService.add_new_user(new_user=new_user, session=session_db)

    if result:
        return {"message": result}
    else:
        raise HTTPException(
            status_code=400,
            detail="Не удалось добавить пользователя"
        )


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(db_connect.get_session)]
):
    result = await UserService.auth_user(session=session, login=form_data.username)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не был найден"
        )
    if not bcrypt_context.verify(form_data.password, result[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пароль не соответствует!"
        )
    else:
        token = await create_access_token(form_data.username, result[-1], timedelta(minutes=15))
        return {"access_token": token, "token_type": "bearer"}


async def create_access_token(username: str, user_id: int, time: timedelta):
    """
    Created and returned jwt token for access
    :param username:
    :param user_id:
    :param time:
    :return:
    """

    encode ={"sub": username, "id": user_id}
    expires = datetime.utcnow() + time
    encode.update({"exp": expires})
    return jwt.encode(encode, auth_key, algorithm=algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Decode jwt
    :param token:
    :return:
    """

    try:
        data = jwt.decode(token, auth_key, algorithms=[algorithm])
        username: str = data.get("sub")
        user_id: int = data.get("id")
        print(user_id, username)

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не действителен"
            )
        else:
            return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не действительный токен"
        )