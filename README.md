# Snowman Labs Backend Challenge

https://github.com/snowmanlabs/backend-challenge


## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.


## Backend local development


- add s3 credential to .env file

```
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=xxxx
AWS_S3_IMAGE_BUCKET=bucketname
```

- start stack with docker compose

```bash
docker-compose up -d
```

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs


- stop stack

```bash
docker-compose down
```

- run tests

 - access bash:
 
```bash
docker-compose exec backend bash
```

 - then type:
 
```bash
pytest
```