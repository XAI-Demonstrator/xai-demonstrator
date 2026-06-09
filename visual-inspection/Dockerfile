FROM node:14-alpine AS builder
ARG FLAVOR="visual-inspection"
ARG MODEL_IDS="my_model"

WORKDIR /

COPY ./inspection-frontend/ .
RUN npm install && export NODE_ENV=production && npm run build -- --mode ${FLAVOR}

RUN apk --no-cache add curl bash unzip
RUN mkdir -p /inspection/model/models && \
    cd /inspection/model/models && \
    curl "https://storage.googleapis.com/xai-demo-assets/visual-inspection/models/my_model.zip" -o "my_model.zip" && \
    unzip -o "my_model.zip" && \
    rm "my_model.zip"

FROM python:3.11-slim

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
COPY inspection-backend/inspection/explainer/explainers/tcav/cavs/ /inspection/explainer/explainers/tcav/cavs/

CMD ["uvicorn", "inspection.main:app", "--host", "0.0.0.0", "--port", "8000"]
