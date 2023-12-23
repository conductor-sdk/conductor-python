# Conductor OSS Python SDK
Python SDK for working with https://github.com/conductor-oss/conductor

[Conductor](https://www.conductor-oss.org/) is an open source distributed, scalable and highly available 
orchestration platform that allows developers to build powerful distributed applications.
You can find the documentation for Conductor here: [Conductor Docs](https://orkes.io/content)

## ⭐ Conductor OSS
Show support for the Conductor OSS.  Please help spread the awareness by starring Conductor repo.

[![GitHub stars](https://img.shields.io/github/stars/conductor-oss/conductor.svg?style=social&label=Star&maxAge=)](https://GitHub.com/conductor-oss/conductor/)

## Content

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Install SDK](#install-sdk)
  - [Setup SDK](#setup-sdk)
- [Build and run hello-world](#build-and-run-hello-world)
- [Implement Worker](#implement-worker)
- [Create a workflow](#create-a-workflow)
  - [Execute workflow synchronously](#execute-workflow-synchronously)
  - [Execute workflow asynchronously](#execute-workflow-asynchronously)
- [Sending Signals to workflow](#sending-signals-to-workflow)
- [Testing your workflows](#testing-your-workflows)
- [Metrics support](#metrics-support)
- [Setup Python Environment](#setup-python-environment)
  - [Server Settings](#server-settings)
  - [Authentication Settings (Optional)](#authentication-settings-optional)
  - [Access Control Setup](#access-control-setup)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Install SDK
Create a virtual environment to build your package
```shell
virtualenv conductor
source conductor/bin/activate
```

Get Conductor Python SDK
```shell
python3 -m pip install conductor-python
```
#### Setup SDK
SDK requires connecting to the Conductor server and optionally supplying with authentication parameters.

```python
from conductor.client.configuration.configuration import Configuration

configuration = Configuration(
    server_api_url='https://play.orkes.io/api',
    debug=False  # set to true for verbose logging
)
```
Configure the authentication settings if your Conductor server requires authentication.
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings

configuration = Configuration(
    authentication_settings=AuthenticationSettings(
        key_id='key',
        key_secret='secret'
    )
)
```

See [Access Control](https://orkes.io/content/docs/getting-started/concepts/access-control) for guide to getting API keys

### Build and run hello-world
Create a `workflow.py`
```python

```

### Implement Worker
### Create a workflow
#### Execute workflow synchronously
#### Execute workflow asynchronously
### Sending Signals to workflow
### Testing your workflows
### Metrics support



