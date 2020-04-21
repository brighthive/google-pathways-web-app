# Google Pathways API

## Getting Started

```bash
# Build the image
docker build -t brighthive/google_pathways_api:latest .
```

```bash
# Stand up the Flaks app and PSQL container
docker-compose -f docker-compose-dev.yml up
```

## Tests

```
pipenv run pytest --log-cli-level=INFO
```