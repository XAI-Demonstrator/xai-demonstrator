# test-local

_This is the local equivalent to the [test-deployment](../test-deployment/)._

Runs the latest version of the XAI Demonstrator with all uses cases as a single Docker application.
Spins up one container for each use case and serves the frontends from a separate NGINX container.
Comes with an all-in-one [Jaeger](https://www.jaegertracing.io/) instance.

## Set up

```bash
docker-compose up
```

Then you can reach
* the XAI Demonstrator's landing page at [localhost:8000](http://localhost:8000)
* the Jaeger UI at [localhost:16686](http://localhost:16686)
