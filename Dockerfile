ARG SDK_ORIGIN=local_sdk

FROM python:3.11-alpine as python_base
RUN mkdir /package
COPY /src /package/src
COPY /setup* /package/
COPY /README.md /package/
WORKDIR /package

FROM python_base as lint
RUN python3 -m pip install pylint
RUN python3 -m pylint --disable=all ./src

FROM python_base as local_sdk
ENV CONDUCTOR_PYTHON_VERSION="v0.0.0"
RUN python3 -m pip install .

FROM python_base as remote_sdk
ARG CONDUCTOR_PYTHON_VERSION
RUN python3 -m pip install conductor-python==${CONDUCTOR_PYTHON_VERSION}

FROM ${SDK_ORIGIN} as python_test_base
RUN rm -rf /package/src
COPY /tests /package/tests

FROM python_test_base as unit_test
RUN python3 -m unittest discover --verbose --start-directory=./tests/unit

FROM python_test_base as integration_test
ARG KEY
ARG SECRET
ARG CONDUCTOR_SERVER_URL
ENV KEY=${KEY}
ENV SECRET=${SECRET}
ENV CONDUCTOR_SERVER_URL=${CONDUCTOR_SERVER_URL}
RUN python3 /package/tests/integration/main.py

FROM python_base as publish
RUN python3 -m pip install setuptools wheel build twine
ARG CONDUCTOR_PYTHON_VERSION
ENV CONDUCTOR_PYTHON_VERSION=${CONDUCTOR_PYTHON_VERSION}
RUN python3 -m build
ARG PYPI_USER
ARG PYPI_PASS
RUN python3 -m twine upload dist/* -u ${PYPI_USER} -p ${PYPI_PASS}
