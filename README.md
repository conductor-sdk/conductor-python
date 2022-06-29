# Netflix Conductor SDK

`conductor-python` repository provides the client SDKs to build Task Workers in Python

## Quick Start

1. [Setup conductor-python package](#Setup-conductor-python-package)
2. [Create and run Task Workers](docs/worker/README.md)
3. [Create workflows using Code](docs/workflow/README.md)
4. [API Documentation](docs/api/README.md)

### Setup conductor python package

Create a virtual environment to build your package:
```shell
virtualenv conductor
source conductor/bin/activate
```

Get Conductor Python SDK
```shell
python3 -m pip install conductor-python
```

### Server Configurations
* server_api_url : Conductor server address.  e.g. `http://localhost:8000/api` if running locally 
* debug: `true` for verbose logging `false` to display only the errors
* authentication_settings: see below
* metrics_settings: see below

### Metrics
Conductor uses [Prometheus](https://prometheus.io/) to collect metrics.

* directory: Directory where to store the metrics 
* file_name: File where the metrics are colleted. e.g. `metrics.log`
* update_interval: Time interval in seconds at which to collect metrics into the file

### Authentication
Use if your conductor server requires authentication
* key_id: Key
* key_secret: Secret for the Key 
