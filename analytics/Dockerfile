FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://github.com/duckdb/duckdb/releases/download/v0.10.2/duckdb_cli-linux-amd64.zip && \
    unzip duckdb_cli-linux-amd64.zip && \
    mv duckdb /usr/local/bin/duckdb && \
    chmod +x /usr/local/bin/duckdb && \
    rm duckdb_cli-linux-amd64.zip && \
    apt-get remove -y wget unzip && \
    apt-get autoremove -y && \
    apt-get clean

COPY analytics/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY analytics /app/

ENV PYTHONPATH=/app

RUN mkdir -p /app/duckdb_data

WORKDIR /app

CMD ["python", "consumer.py"]
