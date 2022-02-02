# test-deployment
![Test Deployment](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Test%20Deployment/badge.svg) ![Monitor Deployment(s)](https://github.com/XAI-Demonstrator/template-service/workflows/Monitor%20Deployment(s)/badge.svg)

_This is the deployment at [https://test.xaidemo.de](https://test.xaidemo.de).
See section [Re-Use](#re-use) for hints how to create a similar deployment elsewhere._

_To run a functionally similar configuration of the XAI Demonstrator locally, see [test-local](../test-local)._

Runs the full XAI Demonstrator with all uses cases as a single Docker application.
Spins up one container for each use case and serves the frontends from a separate NGINX container.
Comes with integrated HTTPS support and an all-in-one [Jaeger](https://www.jaegertracing.io/) instance.

## Connecting to the Jaeger UI

To reach the Jaeger UI, forward the port to your local machine:
```bash
ssh -i <path_to_your_key_file> -L 16686:localhost:16686 ubuntu@test.xaidemo.de
```

Then you can access the Jaeger UI at [localhost:16686](http://localhost:16686).

## Set Up

On a fresh Ubuntu Linux machine:

1. Set up `docker` and make sure that `docker-compose` is installed.
2. Make sure that both port `80` and port `443` are accessible from the outside.
3. Copy the entire `test-deployment` folder and `cd` into `test-deployment`   
4. `cd proxy && ./set-up.sh` to set up the NGINX proxy.
   This step only needs to be repeated if for some reason the NGINX proxy has been shut down.

Everything else is taken care of by the [Test Deployment workflow](../../.github/workflows/test-deployment.yml),
which requires SSH access to pull the container images.

## Re-Use

_If you just want to run an XAI Demonstrator instance locally and do not require HTTPS,
have a look at [test-local](../test-local)._

The `test-deployment` is specific to [https://test.xaidemo.de](https://test.xaidemo.de).

To re-use this configuration elsewhere:

1. Make a copy of the entire `test-deployment` folder
2. Change the domain name and e-mail adress in [proxy/docker-compose.yml](./proxy/docker-compose.yml)
3. If necessary, change the container registry in [docker-compose.yml](./docker-compose.yml) to your own registry
   and/or pin the container images to stable release versions

## Credits

- The proxy configuration for the HTTPS support is taken from
  [letsencrypt-nginx-proxy-companion-compose](https://github.com/buchdag/letsencrypt-nginx-proxy-companion-compose)
  by Nicolas Duchon
