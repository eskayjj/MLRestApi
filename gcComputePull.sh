#!/bin/bash
clear
docker container prune -f
docker run -d --gpus all --rm --name fastapi-docker -p 8080:8080/tcp asia.gcr.io/inspiring-wares-377802/fastapi-docker:latest
docker container ls -a