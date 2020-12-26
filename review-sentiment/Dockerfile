FROM python:3.7-slim

WORKDIR /

COPY ./sentiment-backend /app
COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
