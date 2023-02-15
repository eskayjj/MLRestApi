FROM python:3.10.10-bullseye
WORKDIR /fastapi-docker
COPY ./requirements.txt /fastapi-docker/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /fastapi-docker/requirements.txt
COPY ./app /fastapi-docker/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

FROM nvidia/cuda:12.0-devel
CMD nvidia-smi