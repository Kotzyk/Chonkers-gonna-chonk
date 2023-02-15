# syntax=docker/dockerfile:1
FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
ENV DB_FILE="db/chonkers.db"

COPY . .

CMD [ "python", "./app.py"]