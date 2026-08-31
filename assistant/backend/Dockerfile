FROM python:3.13-alpine

WORKDIR /app

COPY requirements-frozen.txt .
RUN pip install --no-cache-dir -r requirements-frozen.txt

COPY api ./api
COPY llm ./llm

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
