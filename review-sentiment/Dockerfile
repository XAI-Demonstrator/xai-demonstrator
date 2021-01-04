FROM node:12-alpine as builder

WORKDIR /

COPY ./sentiment-frontend/ .
RUN npm install && npm run build

FROM python:3.7-slim

WORKDIR /

COPY sentiment-backend/sentiment /app
COPY sentiment-backend/requirements.txt /requirements.txt
RUN mkdir /app/static
COPY --from=builder /dist/ /app/static/

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

RUN python3 app/model/download_model.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
