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
docker-compose -f docker-compose-test.yml build && docker-compose -f docker-compose-test.yml run test_google_pathways_api && docker-compose -f docker-compose-test.yml down
```