FROM python:3.9-slim

RUN apt-get update
RUN apt-get install --yes iputils-ping

ENV PYTHONPATH="${PYTHONPATH}:/app"

WORKDIR /app

COPY main.py /app/main.py

ENTRYPOINT ["python3", "main.py"]
