from tsk.db.models.UserModel import UserTable
from tsk.db.db_connection import db_connect
from tsk.abs_crud import Crud

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result
from sqlalchemy import select
from tsk.api.models.UserPDModel import AddNewUser
from typing import Union
import asyncio


class UserDbService(Crud):

    @staticmethod
    async def get_one(user_id: int, session: AsyncSession) -> Union[UserTable, bool]:
        """
        Gettind one user by id
        :param user_id:
        :param session:
        :return:
        """

        try:
            user = select(UserTable).where(UserTable.id == user_id)
            user_detail: Result = await session.execute(user)
            information = user_detail.one_or_none()

            if information:
                return information
            raise IndexError
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_all():
        print(2)

    @staticmethod
    async def add_one(new_user: AddNewUser, session: AsyncSession) -> Union[UserTable, bool]:
        """
        Add a new user
        :param new_user:
        :return:
        """
        try:
            new_user = UserTable(
                name_user = new_user.name_user,
                login = new_user.login,
                sex = new_user.sex,
                password = new_user.password
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except Exception as ex:
            return ex
        finally:
            await session.close()

    @staticmethod
    async def update_one(detail: dict):
        print(3)

    @staticmethod
    async def del_one(user_id: int):
        print(4)