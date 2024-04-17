from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from tsk.settings import settings
from tsk.api.models.UserPDModel import UserRequest, Token, AddNewUser
from tsk.api.services.UserService import UserService

from tsk.db.db_connection import db_connect
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from tsk.api.auth.security import Security
from datetime import timedelta


#To authentication user
auth_router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

security_app: Security = Security()


@auth_router.post("/token", response_model=Token)
async def create_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(db_connect.get_session)]
):
    result = await UserService.auth_user(session=session, login=form_data.username)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не был найден"
        )
    if not security_app.bcrypt_context.verify(form_data.password, result[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пароль не соответствует!"
        )
    else:
        token = security_app.create_access_token(form_data.username, result[-1], result[0], timedelta(minutes=5))
        return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/refresh-token", status_code=status.HTTP_201_CREATED)
async def refresh_token(token: str):
    """
    Refresh token
    :param session:
    :param token:
    :return:
    """

    data_to_token: dict = security_app.decode_jwt_token(token=token)
    if data_to_token:
        create_new_token = security_app.create_access_token(
            login=data_to_token.get("login"),
            password=data_to_token.get("password"),
            user_id=data_to_token.get("user_id"),
            date_for_token_time=timedelta(minutes=5)
        )

        return {"access_token": create_new_token, "token_type": "bearer"}