# XAI Demonstrator experiment tracking

- [`data-collector`](./data-collector)
- [`experiment-proxy`](./experiment-proxy)

## Integration tests

Spin up the local version with a dummy use case:
```bash
cd experiment-tracker
docker-compose up --env-file .env.test
```

Run the integration tests:
```bash
cd tests
./run.sh
```
