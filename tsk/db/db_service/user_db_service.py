from db.models.UserModel import UserTable
from abs_crud import Crud
from db.models.PostModel import PostTable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select, update, delete
from sqlalchemy.orm import joinedload
from api.models.UserPDModel import AddNewUser, UserUpdate, User
from typing import Union, List


class UserDbService(Crud):

    @staticmethod
    async def get_one(user_id: int, session: AsyncSession) -> Union[UserTable, bool]:
        """
        Getting one user by id
        :param user_id:
        :param session:
        :return:
        """

        try:
            user = select(UserTable).where(UserTable.id == user_id)
            user_detail: Result = await session.execute(user)
            information: UserTable = user_detail.one_or_none()[0]

            if information:
                return information
            raise IndexError
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_user_and_posts(user_id: int, session: AsyncSession) -> Union[dict, bool]:
        """
        Getting user info and info post by id user
        :param user_id:
        :param session:
        :return:
        """

        try:
            user = select(UserTable).options(joinedload(UserTable.posts)).where(UserTable.id == user_id)
            result: Result = await session.execute(user)
            user_info_all = result.scalar_one_or_none()

            if user_info_all:
                return user_info_all
            raise ValueError
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_all(session: AsyncSession) -> Union[List, List[UserTable]]:
        """
        Getting all users
        :param session:
        :return:
        """

        users = select(UserTable).order_by(UserTable.id)
        users_detail: Result = await session.execute(statement=users)
        data = users_detail.fetchall()

        if data:
            return data
        return []


    @staticmethod
    async def add_one(new_user: AddNewUser, session: AsyncSession) -> bool:
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
                hashed_password = new_user.hashed_password
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return True
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def update_one(user_id: int, session: AsyncSession, update_user: UserUpdate = None) -> bool:
        """
        Update info user by id
        :param update_user:
        :param user_id:
        :param session:
        :return:
        """

        try:
            stmt = update(UserTable).where(UserTable.id == user_id).values(
                **update_user.model_dump()
            )
            await session.execute(statement=stmt)
            await session.commit()
            return True

            raise Exception
        except Exception as ex:
            print(ex)
            return False
        finally:
            await session.close()

    @staticmethod
    async def del_one(user_id: int, session: AsyncSession) -> bool:
        """
        Delete user by id
        :param user_id:
        :return:
        """

        try:
            del_user = delete(UserTable).where(UserTable.id == user_id)
            await session.execute(del_user)
            await session.commit()
            return True
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def update_password(user_id: int, session: AsyncSession, new_password: str) -> bool:
        """
        Update password user
        :param user_id:
        :param session:
        :param new_password:
        :return:
        """

        try:
            stmt = update(UserTable).where(UserTable.id == user_id).values(hashed_password=new_password)
            await session.execute(statement=stmt)
            await session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False
        finally:
            await session.close()