FROM python:2.7.15-slim-jessie
WORKDIR /app
COPY . .
RUN pip install --user tweepy


CMD ["python", "/app/complimentBot.py"]
