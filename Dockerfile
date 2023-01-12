FROM python:3.11-alpine as piton
RUN mkdir /package
COPY /src /package/src
COPY /setup* /package/
WORKDIR /package

FROM piton as lint
RUN python3 -m pip install pylint
RUN python3 -m pylint --disable=all ./src

FROM piton as sdk
ENV CONDUCTOR_PYTHON_VERSION="v0.0.0"
RUN python3 -m pip install .
RUN rm -rf /package/src
COPY /tests /package/tests

FROM sdk as unit_test
RUN python3 -m unittest discover --verbose --start-directory=./tests/unit

FROM sdk as integration_test
ARG KEY
ARG SECRET
ARG CONDUCTOR_SERVER_URL
ENV KEY=${KEY}
ENV SECRET=${SECRET}
ENV CONDUCTOR_SERVER_URL=${CONDUCTOR_SERVER_URL}
RUN python3 /package/tests/integration/main.py
