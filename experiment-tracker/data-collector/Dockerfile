FROM python:3.8-slim

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY tracker /tracker

CMD ["uvicorn", "tracker.main:app", "--host", "0.0.0.0", "--port", "8000"]
