alembic upgrade head; uvicorn app.main:app --host 0.0.0.0 --port 80;
# alembic upgrade head; gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80;