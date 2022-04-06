FROM python:3.9.10-bullseye

COPY . .

RUN python3 -m pip install -r requirements.txt

ENV KEY_VAULT_NAME=$VAULT_NAME

CMD app:api --port=$PORT
ENTRYPOINT ["python3", "-m", "uvicorn"]
