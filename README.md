# XAI Demonstrator
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/XAI-Demonstrator/xai-demonstrator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XAI-Demonstrator/xai-demonstrator/context:javascript)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/XAI-Demonstrator/xai-demonstrator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XAI-Demonstrator/xai-demonstrator/context:python)

The XAI Demonstrator is a modular platform that lets users interact with production-grade Explainable AI (XAI) systems.

**For general information, see our project website at [xai-demonstrator.github.io](https://xai-demonstrator.github.io/).**

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

## Documentation
![Documentation](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Documentation/badge.svg?branch=master)

A technical documentation with user guides is taking shape at [xai-demonstrator.github.io/xai-demonstrator/](https://xai-demonstrator.github.io/xai-demonstrator/).

## Use Cases
Each use case illustrates a particular application of user-centric XAI methods.

Code | Description | Build | Test
-----|-------------|-------|-----
[review-sentiment](/review-sentiment) | Explain the sentiment analysis of customer reviews by a multi-lingual BERT model | ![Review Sentiment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Review%20Sentiment/badge.svg?branch=master) | BE: [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-sentiment-backend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-sentiment-backend)<br />FE: [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-sentiment-frontend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-sentiment-frontend)
[visual-inspection](/visual-inspection) | Visually explain the classification of images | ![Visual Inspection](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Visual%20Inspection/badge.svg?branch=master) | BE: [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-inspection-backend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-inspection-backend)<br />FE: [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-inspection-frontend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-inspection-frontend)

You can try out a standalone version each use case locally by running `docker-compose up` in the respective directory.
Then, the use case is available at [localhost:8000](http://localhost:8000/).

## Further Components

Package | Description | Build | Test
--------|-------------|-------|------
[common/backend-utils](/common/backend-utils) | Python package providing common functionality for FastAPI backend services | ![Backend Utils](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Backend%20Utils/badge.svg?branch=master) | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-backend-utils)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-backend-utils)
[common/vue-components](/common/vue-components) | NPM package providing common VueJS components for frontends | ![Vue Components](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Vue%20Components/badge.svg?branch=master) | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-vue-components)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-vue-components)
[landing-page](/landing-page) | Frontend that serves as a common entry point to all use cases. | ![Landing Page](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Landing%20Page/badge.svg?branch=master) | 

## Deployments
 ![Monitor Deployment(s)](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Monitor%20Deployment(s)/badge.svg)

Configuration | Location | Description | Status
--------------|----------|-------------|-------
[test-deployment](/deployment/test-deployment) | [https://test.xaidemo.de](https://test.xaidemo.de) | Latest version of the landing page and all use cases | ![Test Deployment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Test%20Deployment/badge.svg?branch=master)
[prod-deployment](/deployment/prod-deployment) | [https://www.xaidemo.de](https://www.xaidemo.de) | Current release | ![Prod Deployment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Prod%20Deployment/badge.svg?branch=master)


## License
The XAI Demonstrator is licensed under the terms of the [Apache 2.0 license](LICENSE).
