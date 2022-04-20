from typing import Optional

import pmdarima as pm

from MLSP.app.internal.preprocessing.stock_preprocessing import Ticker, get_ticker_data


# Create an arima model for specified ticker to predict future values
def create_model(ticker: Ticker, train_percentage: Optional[float] = 0.8):
    df = get_ticker_data(ticker.ticker, ticker.date_start, ticker.date_end)

    # Select close column and reshape
    data = df['Close']

    # split into train and test
    train_size = int(len(data) * train_percentage)
    train, test = data[:train_size], data[train_size:]

    # create and train model
    model = pm.auto_arima(train, error_action='ignore', trace=True, suppress_warnings=True, maxiter=10, seasonal=False)

    # Store summary of model
    summary = model.summary().as_text()

    # Predict values
    prediction_days = 10
    predictions = model.predict(prediction_days)

    return predictions, summary
