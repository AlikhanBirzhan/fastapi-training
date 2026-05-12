from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router
from app.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router, prefix='/api/v1', tags=['auth'])
app.include_router(wallet_router, prefix='/api/v1', tags=['wallets'])
app.include_router(operations_router, prefix='/api/v1', tags=['operations'])