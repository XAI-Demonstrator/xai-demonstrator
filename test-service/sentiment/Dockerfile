FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
