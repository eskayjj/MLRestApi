FROM nvidia/cuda:12.0.1-devel-ubuntu22.04
WORKDIR /fastapi-docker

# Install utilities
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl

FROM python:3.10.10-bullseye
WORKDIR /fastapi-docker

# pip install all dependencies
COPY ./requirements.txt /fastapi-docker/requirements.txt
RUN pip3 install --timeout=300 --no-cache-dir --upgrade -r /fastapi-docker/requirements.txt

# Copy app files
COPY ./app /fastapi-docker/app

# Copy GCR commands and run
COPY ./gcr.sh /gcr.sh
RUN chmod +x /gcr.sh

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
