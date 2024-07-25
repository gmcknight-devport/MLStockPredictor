#
FROM python:3.11

#
WORKDIR /MLStockPredictor

#
COPY ./requirements.txt /MLStockPredictor/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /MLStockPredictor/requirements.txt

#
COPY ./MLSP /MLStockPredictor/MLSP

#
CMD ["uvicorn", "MLSP.main:app", "--host", "0.0.0.0", "--port", "80"]
