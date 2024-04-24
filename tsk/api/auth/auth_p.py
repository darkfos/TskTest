from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse

from settings import settings
from api.models.UserPDModel import UserRequest, Token, AddNewUser
from api.services.UserService import UserService

from db.db_connection import db_connect
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from api.auth.security import Security
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
        data_for_token: tuple = security_app.create_access_token(form_data.username, result[-1], result[0], timedelta(minutes=5))
        response: JSONResponse = JSONResponse(content=data_for_token[0])
        response.set_cookie(key="Refresh-token", value=data_for_token[1])
        return response


@auth_router.post("/refresh-token", status_code=status.HTTP_201_CREATED)
async def refresh_token(token: str):
    """
    Refresh token
    :param session:
    :param token:
    :return:
    """

    jwt_access_token: dict = {"access_token": security_app.get_new_token_by_refresh(refresh_token=token),
                              "token_type": "Bearer"}
    return jwt_access_token