from sqlalchemy import select, update, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models.UserModel import UserTable
from db.models.PostModel import PostTable
from abs_crud import Crud
from typing import Union, Annotated, Tuple
from api.models.PostPDModel import UpdatePost


class PostDbService(Crud):
    @staticmethod
    async def get_one(post_id: int, session: AsyncSession) -> Union[bool, PostTable]:
        """
        Get post by id
        :param post_id:
        :return:
        """
        try:
            stmt = select(PostTable).where(PostTable.id == post_id)
            post: Result = await session.execute(statement=stmt)
            result = post.one_or_none()

            if result:
                return result[0]
            raise ValueError
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_all(session: AsyncSession, user_id) -> Union[bool, Tuple[PostTable]]:
        """
        Get all posts
        :return:
        """

        try:
            stmt = select(PostTable).options(joinedload(PostTable.user)).where(PostTable.user_id==user_id)
            posts: Result = await session.execute(statement=stmt)
            results = posts.all()

            if results:
                return results
            raise ValueError
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def add_one(session: AsyncSession, new_post: PostTable) -> bool:
        """
        Add a new post
        :param args:
        :return:
        """

        try:
            session.add(new_post)
            await session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False
        finally:
            await session.close()

    @staticmethod
    async def del_one(session: AsyncSession, id_post: int) -> bool:
        """
        Delete post by id
        :param session:
        :return:
        """

        try:
            stmt = delete(PostTable).where(PostTable.id == id_post)
            await session.execute(statement=stmt)
            await session.commit()
            return True
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def update_one(session: AsyncSession, post_id: int, new_data: UpdatePost) -> True:
        """
        Update data for post
        :param session:
        :param user_id:
        :param new_data:
        :return:
        """

        try:
            stmt = update(PostTable).where(PostTable.id == post_id).values(
                **new_data.model_dump()
            )
            await session.commit()
            return True
        except Exception as ex:
            return False
        finally:
            await session.close()