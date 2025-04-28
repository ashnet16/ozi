FROM python:3.10-slim

WORKDIR /app/rag

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel \
 && pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/rag

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
