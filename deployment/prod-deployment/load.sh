#!/usr/bin/env bash

BASE_URL="${1}"

SENTIMENT_URL="${BASE_URL}/api/sentiment/load"

echo "Place a significant load on the review-sentiment-service to trigger container starts"
seq 1 100 | xargs -Iname -P50 curl -w "%{time_total}" "${SENTIMENT_URL}"

wait
