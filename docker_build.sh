#!/bin/bash
docker buildx build --platform linux/amd64 -t fastapi-docker .
docker images