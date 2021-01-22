FROM node:12-alpine as builder

WORKDIR /

COPY ./inspection-frontend/ .
RUN npm install && npm run build

FROM python:3.8-slim

WORKDIR /

COPY inspection-backend/inspection /inspection
COPY inspection-backend/requirements.txt /requirements.txt
RUN mkdir /inspection/static
COPY --from=builder /dist/ /inspection/static/

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY inspection-backend/trigger_download.py /trigger_download.py
RUN python /trigger_download.py

CMD ["uvicorn", "inspection.main:app", "--host", "0.0.0.0", "--port", "8000"]
g