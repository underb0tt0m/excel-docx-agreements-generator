FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY "cmd/" "./cmd/"
COPY proto/ ./proto/
COPY internal/ ./internal/

ENTRYPOINT ["python", "-m"]
CMD ["cmd.grpc_server.grpc_server"]