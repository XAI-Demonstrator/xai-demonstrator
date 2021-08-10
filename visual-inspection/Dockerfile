FROM node:12-alpine as builder

WORKDIR /

COPY ./inspection-frontend/ .
RUN npm install && npm run build

FROM python:3.8-slim

WORKDIR /

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

COPY inspection-backend/requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY inspection-backend/inspection /inspection

COPY inspection-backend/download_model.sh /download_model.sh
RUN /download_model.sh

RUN mkdir /inspection/static
COPY --from=builder /dist/ /inspection/static/

CMD ["uvicorn", "inspection.main:app", "--host", "0.0.0.0", "--port", "8000"]
