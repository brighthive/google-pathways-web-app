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
Run the tests like so:
```bash
pipenv run pytest
```

You also can run the tests with different options, depending on your needs:
```bash
# Print all logger output to terminal
pipenv run pytest --log-cli-level=INFO
```
```bash
# Do not stop the psql container after running tests
DO_NOT_KILL_DB=true pipenv run pytest
```
