from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Union, List
from db.db_connection import db_connect
from api.models.PostPDModel import AddPost, UpdatePost, GetPost


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

