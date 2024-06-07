FROM python:latest

LABEL Maintainer="Akli RAHMOUN"

COPY ./examples/simple_server.py simple_server.py

RUN python -m pip install c104

EXPOSE 2404

CMD [ "python", "simple_server.py"]
