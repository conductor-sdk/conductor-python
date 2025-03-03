ARG SDK_ORIGIN=no_sdk

FROM python:3.7-alpine as python_base
RUN apk add --no-cache tk

FROM python_base as python_test_base
RUN mkdir -p /package
COPY / /package
WORKDIR /package
RUN pwd
RUN ls -ltr
ENV PYTHONPATH /package/src
RUN python3 -m pip install pylint
#RUN python3 -m pylint --disable=all ./src
RUN python3 -m pip install coverage
RUN python3 -m pip install -r ./requirements.txt

FROM python_test_base as unit_test
ARG CONDUCTOR_AUTH_KEY
ARG CONDUCTOR_AUTH_SECRET
ARG CONDUCTOR_SERVER_URL
ENV CONDUCTOR_AUTH_KEY=${CONDUCTOR_AUTH_KEY}
ENV CONDUCTOR_AUTH_SECRET=${CONDUCTOR_AUTH_SECRET}
ENV CONDUCTOR_SERVER_URL=${CONDUCTOR_SERVER_URL}
RUN ls -ltr
RUN python3 -m unittest discover --verbose --start-directory=./tests/unit
RUN coverage run --source=./src/conductor/client/orkes -m unittest discover --verbose --start-directory=./tests/integration
RUN coverage report -m

FROM python_test_base as test
ARG CONDUCTOR_AUTH_KEY
ARG CONDUCTOR_AUTH_SECRET
ARG CONDUCTOR_SERVER_URL
ENV CONDUCTOR_AUTH_KEY=${CONDUCTOR_AUTH_KEY}
ENV CONDUCTOR_AUTH_SECRET=${CONDUCTOR_AUTH_SECRET}
ENV CONDUCTOR_SERVER_URL=${CONDUCTOR_SERVER_URL}
RUN python3 ./tests/integration/main.py

FROM python:3.11-alpine as publish
RUN apk add --no-cache tk
WORKDIR /package
COPY --from=python_test_base /package /package
ENV PYTHONPATH /package/src
RUN python3 -m pip install -r ./requirements.txt
RUN ls -ltr
RUN python3 -m pip install setuptools wheel build twine
ARG CONDUCTOR_PYTHON_VERSION
ENV CONDUCTOR_PYTHON_VERSION=${CONDUCTOR_PYTHON_VERSION}
RUN python3 -m build
ARG PYPI_USER
ARG PYPI_PASS
RUN python3 -m twine upload dist/* -u ${PYPI_USER} -p ${PYPI_PASS}
