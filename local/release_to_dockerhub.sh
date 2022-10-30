#!/usr/bin/env bash
set -e

echo "Docker Hub: Build & Publish container to repository"

# initialize environment variables
source ./.env
SEMVER=$(cat VERSION)

# Build container image
docker image build \
--build-arg "IMAGE_VERSION=${SEMVER}" \
-f ./Dockerfile -t local/${REPO}:${SEMVER} ./

# Tag image for Testruction's ECR repo
docker image tag \
    local/${REPO}:${SEMVER} \
    docker.io/${REPO}:${SEMVER}

docker image tag \
    local/${REPO}:${SEMVER} \
    docker.io/${REPO}:${SEMVER}-python38

docker image tag \
    local/${REPO}:${SEMVER} \
    docker.io/${REPO}:python38

docker image tag \
    local/${REPO}:${SEMVER} \
    docker.io/${REPO}:${SEMVER}-python38-$(date +%Y%m%d)

docker image tag \
    local/${REPO}:${SEMVER} \
    docker.io/${REPO}:latest

# Push image to Testruction's ECR repo
docker image push \
    docker.io/${REPO} --all-tags