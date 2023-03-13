#!/bin/bash
clear
docker buildx build --platform linux/amd64 -t eskayjj/astar-fastapi-ml .
docker push eskayjj/astar-fastapi-ml:latest