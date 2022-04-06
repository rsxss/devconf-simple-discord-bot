FROM python:3.9.10-bullseye

COPY . .

RUN python3 -m pip install -r requirements.txt

ENV KEY_VAULT_NAME=$VAULT_NAME

ENTRYPOINT gunicorn -b 0.0.0.0:$PORT -w 1 -k uvicorn.workers.UvicornWorker app:api
