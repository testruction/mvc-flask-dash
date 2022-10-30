# MVC Flask Dash

## Introduction 

Ce dépôt contient le ressources permettant tester, assembler, et publier et exécuter le démonstrateur d'application Web Postgres & S3.

## Bien débuter

### Création du fichier .env

```shell
cp -v ./.env.example ./.env
```

### Génération des données Postgres & S3

```shell
export AWS_PROFILE='<profile aws cli>'
source .env

pytest tests/integration/test_s3_a_model.py
pytest tests/integration/test_postgres_a_model.py
```

### Environnement Locale

```shell
export AWS_PROFILE='<profile aws cli>'

local/run_image.sh
```

### Livraison ECR

```shell
export AWS_PROFILE='<profile aws cli>'

local/release_to_ecr.sh
```

### Suppression ECR

```shell
source .env
MSYS_NO_PATHCONV=1 aws cloudformation delete-stack --stack-name "${CNF_ECR_STACK_NAME}"
```
