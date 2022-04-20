from fastapi import FastAPI

from MLSP.app.routers import sentiment_router
from MLSP.app.routers import keras_router

app = FastAPI()

app.include_router(keras_router.router)
app.include_router(sentiment_router.router)
