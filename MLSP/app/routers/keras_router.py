from fastapi import APIRouter, HTTPException
from typing import Optional

from MLSP.app.internal.metrics import RegressionAccuracy
from MLSP.app.internal.keras_predictor.keras_model import ModelOptions, create_model
from MLSP.app.internal.preprocessing.stock_preprocessing import get_processed_ticker_data, Ticker

models = ["LSTM", "SimpleRNN", "Bidirectional", "Conv1D", "GRU"]
activation_functions = ["relu", "sigmoid", "tanh", "softmax", "elu", "softsign", "softplus", "exponential"]


router = APIRouter(
    prefix="/keras",
    responses={404: {"Description": "Couldn't get data, check ticker is correct"}}
)


@router.post("/")
def predict_stock(ticker: Ticker, model_options: ModelOptions, model_name: Optional[str] = "LSTM",
                  activation: Optional[str] = "tanh", train_percentage: Optional[float] = 0.8,
                  time_step: Optional[int] = None):

    try:
        # Check model exists in array:
        if model_name not in models:
            raise HTTPException(status_code=404, detail="Model couldn't be found")

        # If number if iterations is invalid (not between 1 and 10) raise exception
        if not 1 <= model_options.iterations <= 10:
            raise HTTPException(status_code=400, detail="Enter number of iterations between 1 and 10")

        # Preprocessing
        train_x, train_y, test_x, test_y, scale, time_step = get_processed_ticker_data(ticker.ticker, ticker.date_start,
                                                                                       ticker.date_end, train_percentage,
                                                                                       time_step)

        # Check activation function
        if activation not in activation_functions:
            model_options.activation = "tanh"

        # Set input shape and call Keras model
        input_shape = (time_step, 1)
        test_predictions, test_y, future_predictions = create_model(model_name, model_options, input_shape, activation,
                                                                    scale, train_x, train_y, test_x, test_y)

        # calculate accuracy
        metrics = RegressionAccuracy.calc_accuracy(test_predictions[:, 0], test_y[0])

        # Prepare output for JSON encoding
        test_predictions = dict(enumerate(test_predictions.flatten(), 1))
        future_predictions = dict(enumerate(future_predictions.flatten(), 1))

        for i in test_predictions:
            test_predictions[i] = float(test_predictions[i])

        return test_predictions, metrics, future_predictions
    
    except HTTPException:
        import traceback
        return traceback.extract_stack()
