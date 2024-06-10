FROM python:latest

LABEL Maintainer="Akli RAHMOUN"

COPY ./examples/perf_server.py server.py
COPY ./examples/datapoints.json datapoints.json

RUN python -m pip install c104

EXPOSE 2404-2414

CMD [ "python", "./server.py", "./datapoints.json"]
