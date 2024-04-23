from sqlalchemy.ext.asyncio import AsyncSession
from tsk.api.models.UserPDModel import AddNewUser, InformationAboutUser
from tsk.db.db_service.user_db_service import UserDbService

from sqlalchemy import select, Result
from tsk.db.models.UserModel import UserTable
from typing import Union


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
            result: UserTable = to_find_user.one_or_none()[0]
            if result:
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

        user = await UserDbService.get_one(
            user_id=user_id,
            session=session
        )

        print(user)

        if user:
            user_data: InformationAboutUser = InformationAboutUser()
        else:
            return False
