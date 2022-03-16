FROM python:3.9.10-bullseye

COPY . .

EXPOSE 80

RUN python3 -m pip install -r requirements.txt

ENV KEY_VAULT_NAME=$VAULT_NAME

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:80", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:api"]
