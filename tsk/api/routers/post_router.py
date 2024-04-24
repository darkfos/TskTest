from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Union, List, Dict
from db.db_connection import db_connect
from api.models.PostPDModel import AddPost, UpdatePost, GetPost
from api.services.PostService import PostService


#Post router
post_router: APIRouter = APIRouter(
    prefix="/post",
    tags=["Post"]
)


@post_router.get("/get_posts_user")
async def get_all_posts_user(
    session: Annotated[AsyncSession, Depends(db_connect.get_session)],
    token: str
) -> List[GetPost]:
    """
    Get all user posts
    """
    pass


@post_router.post("/create_post")
async def add_new_post(
    session: Annotated[AsyncSession, Depends(db_connect.get_session)],
    token: str,
    new_post: AddPost
) -> Dict[str, str]:
    """
    Add a new post
    """

    is_created_post_from_service: bool = await PostService.create_post_by_user(
        session=session,
        token=token,
        new_post=new_post
        )
    
    if is_created_post_from_service:
        return {"message": "Заметка была успешно создана"}
    else:
        return {"message": "Не удалось создать заметку"}