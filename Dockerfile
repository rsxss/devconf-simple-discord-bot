FROM python:3.9.10-bullseye

COPY . .

RUN python3 -m pip install -r requirements.txt

ENV KEY_VAULT_NAME=$VAULT_NAME

CMD ["-b", "0.0.0.0:80"]
ENTRYPOINT ["gunicorn", "app:api", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
