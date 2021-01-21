# XAI Demonstrator
The XAI Demonstrator is a modular platform that lets users interact with production-grade Explainable AI (XAI) systems.

**For general information and user guides, see our project website at [xai-demonstrator.github.io](https://xai-demonstrator.github.io/)**

## Getting Started
To start a local instance of the XAI Demonstrator, simply run `docker-compose up` in the top-level directory,
wait for all builds to complete and access the app at [localhost:8000](http://localhost:8000/).

## Use Cases
Each use case illustrates a particular application of user-centric XAI methods.

Code | Description | Build | Test
-----|-------------|-------|--------------
[review-sentiment](/review-sentiment) | Explain the sentiment analysis of customer reviews | ![Review Sentiment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Review%20Sentiment/badge.svg) | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-sentiment-backend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-sentiment-backend)
[visual-inspection](/visual-inspection) | Explain the classification of images | ![Visual Inspection](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Visual%20Inspection/badge.svg) | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-inspection-backend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-inspection-backend)


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
