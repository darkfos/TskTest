from fastapi import APIRouter, status, Depends, HTTPException
from tsk.api.models.UserPDModel import AddNewUser
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Optional
from tsk.db.db_connection import db_connect
from tsk.api.services.UserService import UserService
from tsk.api.auth.security import Security
from tsk.api.models.UserPDModel import InformationAboutUser, UserUpdate


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
        token: str
):
    """
    Take info about user by jwt token
    :param session:
    :param token:
    :return:
    """

    user_id: int = security_app.decode_jwt_token(token=token).get("user_id")
    get_to_user: Optional[bool, InformationAboutUser] = await UserService.get_info_user(session=session, user_id=user_id)
    return get_to_user


@user_router.put("/update-user")
async def update_info_about_user(
        session: Annotated[AsyncSession, Depends(db_connect.get_session)],
        token: str,
        user_new_info: UserUpdate,
):
    """
    Update information about user with help jwt token
    :param session:
    :param user_new_info:
    :return:
    """

    user_id_from_token: int = security_app.decode_jwt_token(token=token).get("user_id")
    #Hash password
    user_new_info.hashed_password = security_app.bcrypt_context.hash(user_new_info.hashed_password)
    result = await UserService.update_info_user(session=session, user_data=user_new_info, user_id=user_id_from_token)
    return result


@user_router.put("/update-user-password")
async def update_user_password(
        session: Annotated[AsyncSession, Depends(db_connect.get_session)],
        token: str,
        new_password: str
):
    """
    Update password user
    :param session:
    :param token:
    :param new_password:
    :return:
    """


    result = await UserService.update_password_user(
        session=session,
        token=token,
        user_new_password=new_password
    )
    return result


@user_router.delete("/delete_user")
async def delete_user(
        session: Annotated[AsyncSession, Depends(db_connect.get_session)],
        token: str
):
    """
    Delete user
    :param session:
    :param token:
    :return:
    """

    result = await UserService.del_user_with_id(session=session, token=token)
    return result