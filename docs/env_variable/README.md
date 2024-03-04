# Environment Variable Management

## Env Variable Client

### Initialization
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes.orkes_env_variable_client import OrkesEnvVariableClient

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=False,
    authentication_settings=AuthenticationSettings(key_id=KEY_ID, key_secret=KEY_SECRET)
)

env_variable_client = OrkesEnvVariableClient(configuration)
```

### Saving Environment Variable

```python
env_variable_client.save_env_variable("VAR_NAME", "VAR_VALUE")
```

### Get Environment Variable

#### Get a specific variable

```python
value = env_variable_client.get_env_variable("VAR_NAME")
```

#### Get all variable

```python
var_names = env_variable_client.get_all_env_variables()
```

### Delete Environment Variable

```python
env_variable_client.delete_env_variable("VAR_NAME")
```
