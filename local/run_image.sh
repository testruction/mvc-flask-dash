#!/usr/bin/env bash
set -e

# export DOCKER_BUILDKIT=1

# initialize environment variables
source ./.env

docker-compose up --build --detach

# Check vulnerabilitites
docker container run -it --rm \
-v "${PWD}/build:/root/.cache/" \
-v "/var/run/docker.sock:/var/run/docker.sock"  docker.io/aquasec/trivy image --severity HIGH,CRITICAL image.local/${REPO}

docker-compose exec --user 'root' --workdir '/app' web '/bin/bash'