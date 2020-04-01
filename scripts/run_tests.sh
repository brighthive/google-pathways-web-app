docker-compose -f docker-compose-test.yml build && \
docker-compose -f docker-compose-test.yml run test_google_pathways_api && \
docker-compose -f docker-compose-test.yml down