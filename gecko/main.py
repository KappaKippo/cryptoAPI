from gecko.client import RequestsClient
from gecko.config import settings
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from contextlib import asynccontextmanager
from gecko.storage_interface import StorageManager
from gecko.db import engine
from gecko.models import Coin


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
async def ping(session: Session = Depends(get_session)):
    ping_url = settings.api_url + "ping"
    client = RequestsClient(
        url=ping_url, headers={"x-cg-api-key": settings.api_token}, params={}
    )
    response = client.get()

    return response


@app.get("/coins_list")
async def get_coins(session: Session = Depends(get_session)):
    coins_list_url = settings.api_url + "coins/list"
    client = RequestsClient(
        url=coins_list_url, headers={"x-cg-api-key": settings.api_token}, params={}
    )
    response = client.get()

    storage = StorageManager(session)

    for coin in response:
        storage.create_objects(Coin(**coin))

    storage.commit_and_close()

    return response
