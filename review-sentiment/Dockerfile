FROM node:14-alpine as builder

WORKDIR /

COPY ./sentiment-frontend/ .
RUN npm install && npm run build

FROM python:3.8-slim

WORKDIR /

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

COPY sentiment-backend/requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY sentiment-backend/sentiment /sentiment

COPY sentiment-backend/trigger_download.py /trigger_download.py
RUN python /trigger_download.py

RUN mkdir /sentiment/static
COPY --from=builder /dist/ /sentiment/static/

CMD ["uvicorn", "sentiment.main:app", "--host", "0.0.0.0", "--port", "8000"]
