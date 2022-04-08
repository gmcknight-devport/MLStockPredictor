from fastapi import FastAPI

from .routers.preprocessing import stock_preprocessing

app = FastAPI()

app.include_router(stock_preprocessing.router)
