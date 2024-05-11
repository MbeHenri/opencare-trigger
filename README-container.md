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

* `O3_HOST` - o3 hostname (localhost)
* `O3_PORT` - o3 port (8080)
* `O3_USER` - o3 user (user)
* `O3_PASSWORD` - o3 password (example)
* `MONGO_HOST` - mongo hostname (localhost)
* `MONGO_PORT` - mongo port (27017)
* `BASE_PASSWORD_PATIENT` - base  password of a patient (123456)

## Useful File Locations

* `./build.sh` - Build container
