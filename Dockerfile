FROM python:3.13-slim

ENV PY_ENV=production
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001 5678

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]