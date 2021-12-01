# XAI Demonstrator landing page
![Landing Page](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Landing%20Page/badge.svg?branch=master)

Lets the user navigate between different use cases.

## Components
- Frontend created with [VueJS](https://vuejs.org/)
- [NGINX](https://nginx.org/en/) webserver and proxy configuration

## Configure the frontend build

By default, the landing page frontend includes all use cases.
You can use environment variables to select which use cases are
included in a specific build.
We use the mode-specific `.env` files to configure our standard builds.

| Use Case                                  | Variable     |
|-------------------------------------------|--------------|
| [review-sentiment](../review-sentiment)   | `SENTIMENT`  |
| [visual-inspection](../visual-inspection) | `INSPECTION` |
| [guess-the-country](../guess-the-country) | `COUNTRY`    |

For example, to build a frontend that includes just the [`visual-inspection`](../visual-inspection) use case, set
```dotenv
SENTIMENT=false
INPECTION=true
COUNTRY=false
```

## Build the Docker image

Since the landing page Docker image includes use case frontends,
we need to run `docker build` from the repository's root:

```bash
cd xai-demonstrator/
docker build --file ./landing-page/Dockerfile .
```

Note that the Docker image builds the landing page frontend in
[`test-deployment`](../deployment/test-deployment) configuration.

For details, see the [Dockerfile](./Dockerfile).
