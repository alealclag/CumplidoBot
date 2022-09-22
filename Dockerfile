FROM python:buster
WORKDIR /app
COPY . .
RUN pip install tweepy


CMD ["python", "/app/complimentBot.py"]
