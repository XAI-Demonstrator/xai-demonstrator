# XAI Demonstrator
The XAI Demonstrator is a modular platform that lets users interact with production-grade Explainable AI (XAI) systems.

**For general information and user guides, see our project website at [xai-demonstrator.github.io](https://xai-demonstrator.github.io/)**

## Getting Started
If you just want to try the XAI Demonstrator, have a look at the [list of publicly accessible deployments](#deployments) below.

Running the XAI Demonstrator locally requires [Docker](https://www.docker.com/) (but nothing else).
If you're new to Docker, see [the Docker Desktop installation instructions](https://www.docker.com/products/docker-desktop).

The fastest way to start a local version of the most recent development version of the XAI Demonstrator is to
use the [test-local](./deployment/test-local) deployment configuration:
```bash
cd deployment/test-local
docker-compose up
```
Then, you can reach the app at [localhost:8000](http://localhost:8000/).

To start a local instance of the XAI Demonstrator built from source,
run `docker-compose up` in the top-level directory, wait for all builds to complete,
and access the app at [localhost:8000](http://localhost:8000/).

## Use Cases
Each use case illustrates a particular application of user-centric XAI methods.

Code | Description | Build | Test
-----|-------------|-------|--------------
[review-sentiment](/review-sentiment) | Explain the sentiment analysis of customer reviews | ![Review Sentiment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Review%20Sentiment/badge.svg) | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-sentiment-backend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-sentiment-backend)
[visual-inspection](/visual-inspection) | Explain the classification of images | ![Visual Inspection](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Visual%20Inspection/badge.svg) | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-inspection-backend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-inspection-backend)

You can try out a standalone version each use case locally by running `docker-compose up` in the respective directory.
Then, the use case is available at [localhost:8000](http://localhost:8000/)

## Landing Page
The landing page provides a common entry point to all use cases.

Package | Status
--------|-------
[landing-page](/landing-page) | ![Landing Page](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Landing%20Page/badge.svg)

## Deployments
 ![Monitor Deployment(s)](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Monitor%20Deployment(s)/badge.svg)

Configuration | Location | Description | Status
--------------|----------|-------------|-------
[test-deployment](/deployment/test-deployment) | [https://test.xaidemo.de](https://test.xaidemo.de) | Latest version of the landing page and all use cases | ![Test Deployment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Test%20Deployment/badge.svg)

## License
The XAI Demonstrator is licensed under the terms of the Apache 2.0 license.
