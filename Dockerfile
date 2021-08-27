# syntax=docker/dockerfile:1

FROM python:3.9.6-slim-buster

WORKDIR /app
COPY app.py .
COPY dbcred.py .
COPY templates/ ./templates/
COPY requirements.txt .
RUN pip3 install -r requirements.txt
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
