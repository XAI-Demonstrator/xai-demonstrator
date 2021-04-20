# Customer Review Sentiment Analysis

## Running the service locally (with Docker)

To launch a standalone instance of the service:

```shell
cd review-sentiment
docker-compose up
```

## Running the service locally (without Docker)

During development, it can be desirable to launch the service directly and not as a Docker container.
For instance, this allows to get rapid feedback on changes to the backend code.

```shell
cd review-sentiment
./build_frontend.sh
cd sentiment-backend
uvicorn sentiment.main:app
```
