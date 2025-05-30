FROM python:3.11-slim

WORKDIR /app

COPY server.py .
COPY hello.txt .   

EXPOSE 8080

CMD ["python", "server.py"]