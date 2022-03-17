FROM python:3.9-slim

WORKDIR /

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY backend /backend

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]