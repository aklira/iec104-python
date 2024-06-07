FROM python:latest

LABEL Maintainer="Akli RAHMOUN"

RUN python -m pip install c104

EXPOSE 2404

CMD [ "python", "./examples/simple_server.py"]
