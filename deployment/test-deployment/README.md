# test-deployment
![Test Deployment](https://github.com/XAI-Demonstrator/template-service/workflows/Test%20Deployment/badge.svg) ![Monitor Deployment(s)](https://github.com/XAI-Demonstrator/template-service/workflows/Monitor%20Deployment(s)/badge.svg)

_This is the deployment at [https://test.xaidemo.de](https://test.xaidemo.de)._

Runs the full XAI Demonstrator with all uses cases as a single Docker application.
Spins up one container for each use case and serves the frontends from a separate NGINX container.
Comes with integrated HTTPS support.

## Set Up

On a fresh Ubuntu Linux machine:

1. Set up `docker` and make sure that `docker-compose` is installed.
2. Make sure that both port `80` and port `443` are accessible from the outside.
3. Copy the entire `test-deployment` folder and `cd` into `test-deployment`   
4. `cd proxy && ./set-up.sh` to set up the NGINX proxy.
   This step only needs to be repeated if for some reason the NGINX proxy has been shut down.

Everything else is taken care of by the [Test Deployment workflow](../../.github/workflows/test-deployment.yml),
which requires SSH access and the container registry credentials to pull the container images.

## Re-Use

The configuration here is specific to [https://test.xaidemo.de](https://test.xaidemo.de).

To re-use this deployment elsewhere

1. Make a copy of the entire `test-deployment` folder
2. Change the domain name and e-mail adress in [proxy/docker-compose.yml](./proxy/docker-compose.yml)
3. Change the container registry in [docker-compose.yml](./docker-compose.yml) to your own registry
   (or, if you have access to our registry, at least pin the version)

## Credits

- The proxy configuration for the HTTPS support is taken from
  [letsencrypt-nginx-proxy-companion-compose](https://github.com/buchdag/letsencrypt-nginx-proxy-companion-compose)
  by Nicolas Duchon
