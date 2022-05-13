FROM node:14-alpine as builder
ARG MODEL_IDS="my_model"

WORKDIR /

COPY ./inspection-frontend/ .
RUN npm install && npm run build

RUN apk --no-cache add curl bash unzip
COPY inspection-backend/download_models.sh /download_models.sh
RUN mkdir inspection && mkdir inspection/model && /download_models.sh ${MODEL_IDS} && ls -R inspection/model

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

RUN mkdir /inspection/static && mkdir /inspection/model/my_model
COPY --from=builder /dist/ /inspection/static/
COPY --from=builder /inspection/model/models/ /inspection/model/models/

CMD ["uvicorn", "inspection.main:app", "--host", "0.0.0.0", "--port", "8000"]
