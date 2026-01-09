# ===============================
# 1️⃣ BUILDER STAGE
# ===============================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies for pymssql (uses FreeTDS)
RUN apt-get update && apt-get install -y \
    build-essential \
    freetds-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ===============================
# 2️⃣ RUNTIME STAGE
# ===============================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies for pymssql (FreeTDS libraries)
RUN apt-get update && apt-get install -y \
    freetds-bin \
    libsybdb5 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

WORKDIR /app

ENV PYTHONPATH=/app

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/* \
    && pip install python-multipart \
    && rm -rf /wheels

COPY . .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




# docker build -t resource-service .

# docker run -d --name resource-service --env-file .env -p 8003:8000 resource-service