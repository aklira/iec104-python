FROM python:latest

LABEL Maintainer="Akli RAHMOUN"

COPY ./examples/simple_server.py server.py
COPY ./examples/datapoints.json datapoints.json

RUN python -m pip install c104

EXPOSE 2404

CMD [ "python", "./server.py", "./datapoints.json"]
