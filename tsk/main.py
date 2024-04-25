import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

#from db.db_connection import db_connect
from api.auth.auth_p import auth_router
from api.routers.user_router import user_router
from api.routers.post_router import post_router


application: FastAPI = FastAPI(
    debug="/api/docs"
)

#include routers
application.include_router(
    auth_router
)

application.include_router(
    user_router
)

application.include_router(
    post_router
)


#Redirect to start
@application.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    #asyncio.run(db_connect.create_tables()) - Create Tables
    uvicorn.run(
        app=application
    )