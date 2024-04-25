from sqlalchemy.ext.asyncio import AsyncSession
from api.models.UserPDModel import AddNewUser, InformationAboutUser
from db.db_service.user_db_service import UserDbService

from sqlalchemy import select, Result
from db.models.UserModel import UserTable
from api.models.UserPDModel import SexUser, UserUpdate
from typing import Union, List
from fastapi import HTTPException, status
from api.auth.security import Security
from api.exceptions.user_exception import *


security_apps: Security = Security()


class UserService:

    @staticmethod
    async def add_new_user(session: AsyncSession, new_user: AddNewUser):
        """
        Add a new user
        :param session:
        :param new_user:
        :return:
        """

        add_new_user = await UserDbService.add_one(
            new_user=new_user,
            session=session
        )

        return add_new_user


    @staticmethod
    async def auth_user(session: AsyncSession, login: str) -> Union[bool, tuple]:
        """
        Find user by data
        :param session:
        :param login:
        :param password:
        :return:
        """

        user = select(UserTable).filter(
            UserTable.login == login)
        to_find_user: Result = await session.execute(user)
        if to_find_user:
            result: UserTable = to_find_user.one_or_none()
            if result:
                result = result[0]
                return result.hashed_password, result.id
        return False

    @staticmethod
    async def get_info_user(session: AsyncSession, user_id: int) -> Union[bool, InformationAboutUser]:
        """
        Get user info by user_id
        :param session:
        :param user_id:
        :return:
        """

        user: UserTable = await UserDbService.get_one(
            user_id=user_id,
            session=session
        )

        if user:
            user_data: InformationAboutUser = InformationAboutUser(
                name_user=user.name_user,
                sex=user.sex
            )
            return user_data
        else:
            return False
    
    @staticmethod
    async def get_info_all_users(session: AsyncSession, token: str) -> List[InformationAboutUser]:
        """
        Get information about all users
        """
        
        #decode json

        user_data = security_apps.decode_jwt_token(token=token)

        users = await UserDbService.get_all(session=session)
        users = [InformationAboutUser(name_user=user[0], sex=user[-1]) for user in users]
        return users

    @staticmethod
    async def update_info_user(session: AsyncSession, user_data: UserUpdate, user_id: int) -> dict:
        """
        Update information user service
        :param session:
        :param user_id:
        :param name_user:
        :param sex:
        :return:
        """

        result = await UserDbService.update_one(session=session, update_user=user_data, user_id=user_id)
        if result: return {"message": True}
        else:
            await http_406_error_update_user()

    @staticmethod
    async def update_password_user(session: AsyncSession, token: str, user_new_password: str) -> dict:
        """
        Update user password
        :param session:
        :param user_new_password:
        :param user_id:
        :return:
        """

        #Get user id
        user_id: int = security_apps.decode_jwt_token(token=token).get("user_id")
        user_new_password = security_apps.bcrypt_context.hash(user_new_password)
        result = await UserDbService.update_password(user_id=user_id, session=session, new_password=user_new_password)
        if result:
            return {"message": "Пароль был успешно обновлен!"}
        else:
            await http_400_error_with_update_password_user()

    @staticmethod
    async def del_user_with_id(session: AsyncSession, token: str):
        """
        Delete user
        :param session:
        :param token:
        :return:
        """

        #Get user_id
        user_id: int = security_apps.decode_jwt_token(token=token).get("user_id")
        db_service_request = await UserDbService.del_one(
            user_id=user_id,
            session=session
        )

        if db_service_request: return {"message": "Пользователь был успешно удален"}
        else:
            await http_400_error_delete_user()