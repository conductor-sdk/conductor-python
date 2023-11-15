# Secret Management

## Secret Client

### Initialization
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes_clients import OrkesClients

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=False,
    authentication_settings=AuthenticationSettings(key_id=KEY_ID, key_secret=KEY_SECRET)
)

orkes_clients = OrkesClients(configuration)
secret_client = orkes_clients.getSecretClient()
```

### Saving Secret
```python
secret_client.putSecret("SECRET_NAME", "SECRET_VALUE")
```

### Get Secret

#### Get a specific secret value
```python
value = secret_client.getSecret("SECRET_NAME")
```

#### List all secret names
```python
secret_names = secret_client.listAllSecretNames()
```

#### List all secret names that user can grant access to
```python
secret_names = secret_client.listSecretsThatUserCanGrantAccessTo()
```

### Delete Secret
```python
secret_client.deleteSecret("SECRET_NAME")
```

### Secret Tag Management

#### Set secret tags
```python
from conductor.client.orkes.models.metadata_tag import MetadataTag

tags = [
    MetadataTag("sec_tag", "val"), MetadataTag("sec_tag_2", "val2")
]
secret_client.setSecretTags(tags, "SECRET_NAME")
```

#### Get secret tags
```python
tags = secret_client.getSecretTags("SECRET_NAME")
```

#### Delete secret tags
```python
tags = [
    MetadataTag("sec_tag", "val"), MetadataTag("sec_tag_2", "val2")
]
secret_client.deleteSecretTags(tags, "SECRET_NAME")
```
