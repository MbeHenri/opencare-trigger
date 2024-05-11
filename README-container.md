# Docker Container

## build

```sh
docker build -t opencare-trigger .
```

## run

```sh
docker run --env-file ./example.env opencare-trigger [--network <network_name>]
```

## Environment Variables

* `O3_HOST` - o3 host 📌
* `O3_PORT` - o3 port (80)
* `O3_USER` - o3 user 📌
* `O3_PASSWORD` - o3 password 📌
* `MONGO_HOST` - mongo hostname 📌
* `MONGO_PORT` - mongo port (27017)
* `MONGO_USER` - mongo user used (define for authentification)
* `MONGO_PASSWORD` - password of mongo user (define for authentification)
* `BASE_PASSWORD_PATIENT` - base  password of a patient (123456)
