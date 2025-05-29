FROM python:3.12-slim

ENV PYTHONPATH=$PYTHONPATH:/app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN pytest tests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]