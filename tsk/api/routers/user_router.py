from fastapi import APIRouter, status, Depends, HTTPException
from tsk.api.models.UserPDModel import AddNewUser
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from tsk.db.db_connection import db_connect
from tsk.api.services.UserService import UserService
from tsk.api.auth.security import Security


user_router: APIRouter = APIRouter(
    prefix="/user",
    tags=["User"]
)

security_app: Security = Security()


@user_router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def register_user(new_user: AddNewUser, session: Annotated[AsyncSession, Depends(db_connect.get_session)]):
    """
    Create a new user
    :param new_user:
    :param session:
    :return:
    """

    #Hash password
    new_user.password = security_app.bcrypt_context.hash(new_user.password)
    result_add_user = await UserService.add_new_user(
        new_user=new_user,
        session=session
    )

    if result_add_user:
        return {"message": "Пользователь был успешно зарегистрирован!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось создать пользователя!"
        )


@user_router.get("/user_info")
async def information_about_user(
        session: Annotated[AsyncSession, Depends(db_connect.get_session)],
        token: Annotated[str, Depends(security_app.oauth2_bearer)]
):
    """
    Take info about user by jwt token
    :param session:
    :param token:
    :return:
    """

    user_id: int = security_app.decode_jwt_token(token=token).get("user_id")
    get_to_user = UserService.get_info_user(session=session, user_id=user_id)

    return {"message": "Долбаеб?"}