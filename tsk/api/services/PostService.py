from api.auth.security import Security
from typing import Union, List, Annotated
from fastapi import status, HTTPException
from db.db_service.post_db_service import PostDbService
from api.models.PostPDModel import AddPost, GetPost, UpdatePost
from db.models.PostModel import PostTable

from sqlalchemy.ext.asyncio import AsyncSession


security_apps: Security = Security()


class PostService:

    @staticmethod
    async def get_all_posts_for_user(
        session: AsyncSession,
        token: str
    ) -> Union[List, List[GetPost]]:
        """
            Get all posts for user
        """

        #Get user_id
        user_id: int = security_apps.decode_jwt_token(token=token).get("user_id")
        
        posts = await PostDbService.get_all(session=session, user_id=user_id)

        if posts:
            all_posts: List[GetPost] = [
                GetPost(
                    title=post[0].title,
                    description=post[0].description,
                    date_create=post[0].date_create,
                    user_create=post[0].user.name_user
                )
                for post in posts
            ]

            return all_posts
        else:
            return []
    
    @staticmethod
    async def create_post_by_user(
        session: AsyncSession,
        token: str,
        new_post: AddPost
    ) -> bool:
        """
        Create post by user
        """

        #Get user id
        user_id: int = security_apps.decode_jwt_token(token=token).get("user_id")
        post_object: PostTable = PostTable(
            title = new_post.title,
            description = new_post.description,
            date_create = new_post.date_create,
            user_id = user_id
        )

        is_created_user: bool = await PostDbService.add_one(session=session, new_post=post_object)

        return is_created_user