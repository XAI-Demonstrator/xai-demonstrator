#!/usr/bin/env bash

export COUCHDB_URL=http://localhost:8002
export COLLECTOR_URL=http://localhost:8001
export PROXY_URL=http://localhost:8000
export SERVICE_URL=http://localhost:8003

export SERVICE_NAME="integration_tests"

pytest integration/
