FROM python:3.14.10-alpine3.24
WORKDIR /app
COPY bot/ bot/
CMD ["python", "-B", "-u", "-m", "bot"]
