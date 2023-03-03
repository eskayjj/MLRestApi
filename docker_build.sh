#!/bin/bash
clear
docker buildx build --platform linux/amd64 -t fastapi-docker .
docker container prune -f
docker run -d -it --rm --gpus all --name fastapi-docker -p 80:8080/tcp fastapi-docker
docker container ls -a