FROM python:3.9.10-bullseye

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD ["--port=80"]
ENTRYPOINT ["uvicorn", "app:api"]