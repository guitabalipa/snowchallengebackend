# Snowman Labs Backend Challenge


Backend challenge created with FastAPI.



https://github.com/tiangolo/fastapi

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

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc


- stop stack

```bash
docker-compose down
```

Run Tests:

 - access bash:
 
```bash
docker-compose exec backend bash
```

 - then type:
 
```bash
pytest
```


Heroku: https://vast-anchorage-57708.herokuapp.com/docs#/
Postmam collection: https://www.getpostman.com/collections/51d5bd978ee9e41f2cdd


