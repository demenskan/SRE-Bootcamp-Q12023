FROM python:3-alpine
#FROM python:3.8.5-alpine3.11

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ENTRYPOINT python api.py
# Add your instructions to dockerize the application
# App must run on port 8000
# para correr el contenedor temporalmente:
# docker container run -d -p 8000:8000 -v "${PWD}:/usr/src/app" --name bootcamp bootcamp:v1
