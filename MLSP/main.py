from fastapi import FastAPI

from MLSP.app.routers import sentiment_router, ma_router
from MLSP.app.routers import keras_router

description = """
The API allows a user to explore the accuracy of Keras stock prediction, statistical analysis stock prediction, and 
sentiment analysis in relation to stocks on twitter and through financial news headlines. 

In contrast to most online tutorials the user should see the relative ineffectiveness of Keras ML models and the 
slightly better effectiveness of Arima for prediction. The key issue is the random walk hypothesis - stock data is 
random and unpredictable when only considering the data. The models will copy the last step when predicting on test 
data giving a false sense of accuracy, the issues are more easily seen when plotting the data and predicting future 
values wherein the output converges on the same number after a period of steps. 

Sentiment analysis can have a much better impact on accuracy, social factors play a significant role in price movements 
of shares - consider the effect Elon Musk's tweets have on cryptocurrency purchasing and their resultant worth. 

High volume and short time scale investing can be aided with current computing capabilities but the long term is best 
avoided with these tools. 
"""
app = FastAPI(title="Machine Learning Stock Predictor", description=description)

app.include_router(keras_router.router)
app.include_router(sentiment_router.router)
app.include_router(ma_router.router)
