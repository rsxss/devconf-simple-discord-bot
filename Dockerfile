FROM python:3.9.10-bullseye

COPY . .

RUN python3 -m pip install -r requirements.txt

ENV KEY_VAULT_NAME=$VAULT_NAME

CMD ["app:api", "-b", "0.0.0.0:$PORT"]
ENTRYPOINT ["python", "-m", "uvicorn"]
