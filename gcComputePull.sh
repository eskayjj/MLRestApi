#!/bin/bash
clear
docker container prune -f
docker run -d --gpus all --rm --name fastapi-docker -p 8080:8080/tcp asia.gcr.io/inspiring-wares-377802/fastapi-docker@sha256:5a1d726ce152338630adaa938c4dcea677b63a1e5314358ece4a37f09303c776
docker container ls -a