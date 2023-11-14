# Exception Handling

## APIErrorCode

These are the error codes that are returned when any of the Orkes Clients throw an exception.

| Code  | Accessor | Description |
| --- | --- | --- |
|"NOT_FOUND"|APIErrorCode.NOT_FOUND|Object not found|
|"FORBIDDEN"|APIErrorCode.FORBIDDEN|Access to object is forbidden|
|"CONFLICT"|APIErrorCode.CONFLICT|Object already exists|
|"BAD_REQUEST"|APIErrorCode.BAD_REQUEST|Request not formed correctly|
|"REQUEST_TIMEOUT"|APIErrorCode.REQUEST_TIMEOUT|Request timed out|
|"UNKNOWN"|APIErrorCode.UNKNOWN|Unknown error|

## APIError

This is the exception that is thrown when an Orkes Client related SDK API method fails or returns an error.

```python
from conductor.client.exceptions.api_error import APIError, APIErrorCode
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient

WORKFLOW_NAME = 'test_workflow'

auth = AuthenticationSettings(key_id=KEY_ID, key_secret=KEY_SECRET)
config = Configuration(server_api_url=SERVER_API_URL, authentication_settings=auth)
metadata_client = OrkesMetadataClient(config)

try:
    metadata_client.getWorkflowDef(WORKFLOW_NAME, 1)
except APIError as e:
    if e.code == APIErrorCode.NOT_FOUND:
        print(f"Error finding {WORKFLOW_NAME}: {e.message}")
    elif e.code == APIErrorCode.FORBIDDEN:
        print(f"Error accessing {WORKFLOW_NAME}: {e.message}")
    else:
        print(f"Error fetching {WORKFLOW_NAME}: {e.message}")
    
```
