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


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        session_db: Annotated[AsyncSession, Depends(db_connect.get_session)],
        new_user: AddNewUser) -> dict:

    new_user.password = security_app.bcrypt_context.hash(new_user.password)
    result = await UserService.add_new_user(new_user=new_user, session=session_db)

    if result:
        return {"message": "Пользователь был успешно зарегистрирован!"}
    else:
        raise HTTPException(
            status_code=400,
            detail="Не удалось добавить пользователя"
        )


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
        token = security_app.create_access_token(form_data.username, result[-1], timedelta(minutes=15))
        return {"access_token": token, "token_type": "bearer"}