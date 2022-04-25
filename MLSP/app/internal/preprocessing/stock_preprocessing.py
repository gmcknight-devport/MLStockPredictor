from fastapi import HTTPException
from typing import Optional
from sklearn.preprocessing import MinMaxScaler
from pydantic import BaseModel
import math

import yfinance as yf
from datetime import date as date, timedelta
import numpy as np


class Ticker(BaseModel):
    ticker: str
    date_start: date
    date_end: date


# Return raw data for ticker between specified dates
def get_ticker_data(ticker: str, date_start: date, date_end: date):
    yf_ticker = yf.Ticker(ticker)
    df = yf_ticker.history(start=date_start, end=date_end, interval="1d")

    if df.empty:
        raise HTTPException(status_code=404, detail="Couldn't get data, check ticker is correct and dates provided")
    else:
        return df


# Return preprocessed data for ticker between specified dates
# Reshapes, scales, and splits data into train and test
def get_processed_ticker_data(ticker: str, date_start: date, date_end: date, train_percentage: Optional[float] = 0.8,
                              time_step: Optional[int] = None):

    # Ensure enough data retrieved for split - taking account of weekends
    if date_end - date_start < timedelta(days=10):
        date_start = date_end - timedelta(days=10)

    # Get ticker data
    df = get_ticker_data(ticker, date_start, date_end)

    # Select close column and reshape
    data = df.loc[:, ['Close']]

    # normalize the dataset
    scale = MinMaxScaler(feature_range=(0, 1))
    data_sc = scale.fit_transform(data)

    # split into train and test
    train_size = int(len(data_sc) * train_percentage)
    test_size = len(data_sc) - train_size

    # Split into train and test
    train, test = data_sc[0:train_size, :], data_sc[train_size:len(data_sc), :]

    # Ensure time step is set to an appropriate value - at least a 6th of total data size
    if time_step is None or time_step > (0.16 * len(data_sc)):
        days = len(data_sc)
        time_step = math.ceil(days * .1)

    # split into x and y
    train_x, train_y = __split_x_y(train, time_step)
    test_x, test_y = __split_x_y(test, time_step)

    # reshape x, manually assign batch step if necessary
    train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))
    if len(test_x) == 1:
        test_x = np.reshape(test_x, (1, test_x.shape[1], 1))
    else:
        test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))

    return train_x, train_y, test_x, test_y, scale, time_step


# Split dataset by time step
def __split_x_y(dataset, timestep):
    x, y = [], []
    for i in range(len(dataset) - timestep):
        x.append(dataset[i:(i + timestep), 0])
        y.append(dataset[i + timestep, 0])
    return np.array(x), np.array(y)
