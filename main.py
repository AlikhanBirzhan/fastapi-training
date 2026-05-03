from fastapi import FastAPI

from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operations_router
from app.database import Base, engine

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Подключаем роутер для кошельков с префиксом /api/v1
app.include_router(wallet_router, prefix='/api/v1', tags=['wallet'])
# Подключаем роутер для операции с префиксом /api/v1
app.include_router(operations_router, prefix='/api/v1', tags=['operations'])

Base.metadata.create_all(bind=engine)