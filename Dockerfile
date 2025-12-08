FROM python:3.12-slim

WORKDIR /app

COPY api ./api
COPY model ./model
COPY data ./data
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]