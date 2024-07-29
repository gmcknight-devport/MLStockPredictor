from typing import Optional
from datetime import date, timedelta

from fastapi import APIRouter

from MLSP.app.internal.moving_average_model.arima import create_model
from MLSP.app.internal.preprocessing.stock_preprocessing import Ticker

router = APIRouter(
    prefix="/statistical",
    responses={404: {"Description": "Couldn't get data, check path and variables are correct"}}
)


@router.post('/arima')
def arima_model(ticker: Ticker, train_percentage: Optional[float] = 0.8):

    # Ensure enough days for model to run properly
    if ticker.date_end - ticker.date_start < timedelta(days=7):
        ticker.date_start -= timedelta(days=7)

    predictions, summary = create_model(ticker, train_percentage)

    # Prepare output for JSON encoding
    predictions = dict(enumerate(predictions.to_numpy().flatten(), 1))

    return predictions, summary
