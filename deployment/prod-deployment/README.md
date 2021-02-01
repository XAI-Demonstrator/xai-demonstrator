# test-deployment
![Test Deployment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Prod%20Deployment/badge.svg)
![Monitor Deployment(s)](https://github.com/XAI-Demonstrator/template-service/workflows/Monitor%20Deployment(s)/badge.svg)

_This is the deployment currently at [xai-demonstrator-test.web.app](http://xai-demonstrator-test.web.app/) 
that will soon move to its final home at [https://www.xaidemo.de](https://www.xaidemo.de)._

Production deployment of the XAI demonstrator on [Google Cloud Platform](https://cloud.google.com).
The frontend is served through [Firebase Hosting](https://firebase.google.com/docs/hosting/)
with the backends deployed on [Google Cloud Run](https://cloud.google.com/run/).

## Set Up [WIP]

Requires a GCP project with enabled Cloud Run, which in turn requires Google Container Registry (GCR).
A service account that can push to GCR and deploy to Cloud Run has to be configured.
For the frontends, an associated Firebase Hosting project has to be created.

Everything else is taken care of by the [Prod Deployment workflow](../../.github/workflows/prod-deployment.yml).
This workflow requires the access tokens and some GCP configuration to be provided as secrets.
