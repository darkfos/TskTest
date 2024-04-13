import asyncio
import uvicorn

from fastapi import FastAPI
from db.db_connection import db_connect

application: FastAPI = FastAPI()

if __name__ == "__main__":
    #asyncio.run(db_connect.create_tables()) - Create Tables
    uvicorn.run(
        app=application
    )