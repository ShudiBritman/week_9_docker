# Docker Commands

Fill in the Docker commands you used to complete the test.

## Volume

### Create the volume

```bash
docker volume create fastapi-db
```

### Seed the volume (via Docker Desktop)

```bash

```

## Server 1

### Build the image

```bash
docker build -t shopping_server1:v1 .
```

### Run the container

```bash
docker run -it --name my_server1 -p 8000:8000 -v fastapi-db:/app/db shopping_server1:v1
```

## Server 2

### Build the image

```bash
docker build -t shopping_server2:v1 .
```

### Run the container

```bash
docker run -it --name my_server2 -p 8080:8080 -v fastapi-db:/app/db shopping_server2:v1
```

