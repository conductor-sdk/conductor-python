# swagger_client.QueueAdminResourceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**names**](QueueAdminResourceApi.md#names) | **GET** /api/queue/ | Get Queue Names
[**size1**](QueueAdminResourceApi.md#size1) | **GET** /api/queue/size | Get the queue length
[**update1**](QueueAdminResourceApi.md#update1) | **POST** /api/queue/update/{workflowId}/{taskRefName}/{status} | Publish a message in queue to mark a wait task as completed.
[**update_by_task_id**](QueueAdminResourceApi.md#update_by_task_id) | **POST** /api/queue/update/{workflowId}/task/{taskId}/{status} | Publish a message in queue to mark a wait task (by taskId) as completed.

# **names**
> dict(str, str) names()

Get Queue Names

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.QueueAdminResourceApi()

try:
    # Get Queue Names
    api_response = api_instance.names()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueAdminResourceApi->names: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**dict(str, str)**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **size1**
> dict(str, int) size1()

Get the queue length

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.QueueAdminResourceApi()

try:
    # Get the queue length
    api_response = api_instance.size1()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueAdminResourceApi->size1: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**dict(str, int)**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update1**
> update1(body, workflow_id, task_ref_name, status)

Publish a message in queue to mark a wait task as completed.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.QueueAdminResourceApi()
body = NULL # dict(str, object) | 
workflow_id = 'workflow_id_example' # str | 
task_ref_name = 'task_ref_name_example' # str | 
status = 'status_example' # str | 

try:
    # Publish a message in queue to mark a wait task as completed.
    api_instance.update1(body, workflow_id, task_ref_name, status)
except ApiException as e:
    print("Exception when calling QueueAdminResourceApi->update1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**dict(str, object)**](dict.md)|  | 
 **workflow_id** | **str**|  | 
 **task_ref_name** | **str**|  | 
 **status** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_by_task_id**
> update_by_task_id(body, workflow_id, task_id, status)

Publish a message in queue to mark a wait task (by taskId) as completed.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.QueueAdminResourceApi()
body = NULL # dict(str, object) | 
workflow_id = 'workflow_id_example' # str | 
task_id = 'task_id_example' # str | 
status = 'status_example' # str | 

try:
    # Publish a message in queue to mark a wait task (by taskId) as completed.
    api_instance.update_by_task_id(body, workflow_id, task_id, status)
except ApiException as e:
    print("Exception when calling QueueAdminResourceApi->update_by_task_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**dict(str, object)**](dict.md)|  | 
 **workflow_id** | **str**|  | 
 **task_id** | **str**|  | 
 **status** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

