import asyncio
import uvicorn

from fastapi import FastAPI

from db import MainBase

application: FastAPI = FastAPI()
MainBase.metadata.create_all


if __name__ == "__main__":
    uvicorn.run(
        app=application
    )