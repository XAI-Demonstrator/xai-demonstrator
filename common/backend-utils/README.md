# XAI Demonstrator backend utilities
![Backend Utils](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Backend%20Utils/badge.svg?branch=master)

Python package that provides shared functionality for _XAI Demonstrator_ backend microservices.

## Modules

- [`xaidemo.routers`](./xaidemo/routers.py): FastAPI routers
- [`xaidemo.tracing`](./xaidemo/tracing.py): OpenTelemetry tracing instrumentation and configuration
- [`xaidemo.http_client`](./xaidemo/http_client.py): `aiohttp` based async HTTP client
- [`xaidemo.tracking`](./xaidemo/tracking): Utilities for recording data during experiments with users
