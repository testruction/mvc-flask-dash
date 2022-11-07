# MVC Flask Dash

## Introduction 

This repository provides resources allowing to test, build, and publish a Python Flask based Web application relying on the MVC model.

## Getting started

The `.env` file contains the required the component adressing and associated credentials.
Run the following command to copy from the example file provided in this repository.

```shell
cp -v ./.env.example ./.env
```

Run the Docker stack

```shell
docker-compose up -d --build
```

Access the Web application at <http://localhost:55000>.


## Testing

Application components can be tested individually using pytest.

```shell
pytest tests/integration/test_a_model.py
```
