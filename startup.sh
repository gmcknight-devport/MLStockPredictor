# gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
python -m uvicorn main:app --host 0.0.0.0
