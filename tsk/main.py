import asyncio
import uvicorn

from fastapi import FastAPI

#from db.db_connection import db_connect
from tsk.api.auth.auth_p import auth_router
from tsk.api.routers.user_router import user_router


application: FastAPI = FastAPI()

#include routers
application.include_router(
    auth_router
)
application.include_router(
    user_router
)


if __name__ == "__main__":
    #asyncio.run(db_connect.create_tables()) - Create Tables
    uvicorn.run(
        app=application
    )