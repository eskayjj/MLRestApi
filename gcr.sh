#!/bin/bash

docker tag fastapi-docker asia.gcr.io/inspiring-wares-377802/ml-fastapi

docker images

docker push asia.gcr.io/inspiring-wares-377802/ml-fastapi:latest

gcloud run deploy ml-fastapi --image asia.gcr.io/inspiring-wares-377802/ml-fastapi --memory 4G --region asia-southeast1 --platform managed --port 8080