# gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
python -m uvicorn application:app --host 0.0.0.0
