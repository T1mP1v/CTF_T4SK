FROM python:3.11-slim
# FROM nvidia/cuda:12.1.0-base-ubuntu22.04 if use gpu
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8888

CMD ["gunicorn", "app.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--workers", "1", \
     "--threads", "8", \
     "--bind", "0.0.0.0:8888", \
     "--timeout", "120", \
     "--keep-alive", "120"]
