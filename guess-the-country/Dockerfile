FROM node:14-alpine as builder

WORKDIR /

COPY ./country-frontend/ .
RUN npm install && npm run build

RUN apk --no-cache add curl bash unzip
COPY country-backend/download_model.sh /download_model.sh
RUN mkdir country && mkdir country/model && /download_model.sh && ls -R country/model

FROM python:3.8-slim

WORKDIR /

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get install ffmpeg libsm6 libxext6  -y \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

COPY country-backend/requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY country-backend/country /country

RUN mkdir /country/static && mkdir /country/model/my_model
COPY --from=builder /dist/ /country/static/
COPY --from=builder /country/model/my_model /country/model/my_model/

CMD ["uvicorn", "country.main:app", "--host", "0.0.0.0", "--port", "8000"]
