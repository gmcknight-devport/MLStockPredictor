from keras import Sequential
from keras.activations import relu, sigmoid, tanh, softmax, elu, softsign, softplus, exponential
from keras.layers import Dropout, Dense, LSTM, Conv1D, SimpleRNN, Bidirectional, GRU
from typing import Optional, Type
from pydantic import BaseModel
import numpy as np
from sklearn.preprocessing import MinMaxScaler


models = {"LSTM": LSTM, "SimpleRNN": SimpleRNN, "Bidirectional": Bidirectional, "Conv1D": Conv1D, "GRU": GRU}
activation_functions = {"relu": relu, "sigmoid": sigmoid, "tanh": tanh, "softmax": softmax, "elu": elu,
                        "softsign": softsign, "softplus": softplus, "exponential": exponential}


class ModelOptions(BaseModel):
    iterations: Optional[int] = 1
    epochs: Optional[int] = 20
    num_inputs: Optional[object] = 40
    batch_size: Optional[int] = 10
    dropout: Optional[float] = 0.1
    optimiser: Optional[str] = "adam"
    loss: Optional[str] = "mse"


def create_model(model_name: type, keras_model_options: ModelOptions, input_shape: object, activation_function: type,
                 scale: MinMaxScaler, train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray, test_y: np.ndarray):

    # Check activation function exists in array:
    if activation_function not in activation_functions.keys():
        activation_function = activation_functions.get("tanh")
    else:
        activation_function = activation_functions.get(activation_function)

    # Create sequential model
    model = Sequential()

    # Set batch size if it's None
    if keras_model_options.batch_size is None:
        keras_model_options.batch_size = len(train_x[0]) * 0.025
        keras_model_options.batch_size = round(keras_model_options.batch_size)

    # loop iterations 1 less than parameter to include return_sequences
    for i in range(keras_model_options.iterations - 1):
        model.add(model_name(keras_model_options.num_inputs, input_shape=input_shape, activation=activation_function,
                             return_sequences=True))
        model.add(Dropout(keras_model_options.dropout))

    # Add last layer of model with dropout and dense
    model.add(model_name(keras_model_options.num_inputs, input_shape=input_shape, activation=activation_function))
    model.add(Dropout(0.1))
    model.add(Dense(1, activation=activation_function))

    # Compile model
    model.compile(
        optimizer=keras_model_options.optimiser,
        loss=keras_model_options.loss,
        metrics=['accuracy'])

    # Fit model
    model.fit(train_x, train_y, epochs=keras_model_options.epochs, batch_size=keras_model_options.batch_size, verbose=1)

    # Convert values to float from numpy.int32
    test_x = test_x.astype(float)
    test_y = test_y.astype(float)

    # Make test predictions
    test_predictions = model.predict(test_x)

    # Invert scaling
    test_predictions = scale.inverse_transform(test_predictions)
    test_y = scale.inverse_transform([test_y])

    # Future Predictions
    prediction_days = 10
    predictions = np.array([])

    # Get most recent Close value and prepare for prediction
    last_val = test_y[-1]
    last_val = last_val[-1]
    last_val = np.reshape(last_val, (1, 1, 1))
    p = last_val

    # Predict next close price based on previous
    for i in range(prediction_days):
        p = model.predict(p)
        p = np.reshape(p, (1, p.shape[0], p.shape[1]))
        predictions = np.append(predictions, p)

    # Reshape and scale predictions
    predictions = np.reshape(predictions, (predictions.shape[0], 1))
    predictions = scale.inverse_transform(predictions)

    return test_predictions, test_y, predictions
