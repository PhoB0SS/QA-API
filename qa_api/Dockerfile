FROM python:3.12
LABEL authors="Artem Plotnikov"

WORKDIR /home

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY qa_api ./qa_api
COPY alembic.ini .
COPY config.py .