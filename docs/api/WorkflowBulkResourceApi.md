# swagger_client.WorkflowBulkResourceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pause_workflow1**](WorkflowBulkResourceApi.md#pause_workflow1) | **PUT** /api/workflow/bulk/pause | Pause the list of workflows
[**restart1**](WorkflowBulkResourceApi.md#restart1) | **POST** /api/workflow/bulk/restart | Restart the list of completed workflow
[**resume_workflow1**](WorkflowBulkResourceApi.md#resume_workflow1) | **PUT** /api/workflow/bulk/resume | Resume the list of workflows
[**retry1**](WorkflowBulkResourceApi.md#retry1) | **POST** /api/workflow/bulk/retry | Retry the last failed task for each workflow from the list
[**terminate**](WorkflowBulkResourceApi.md#terminate) | **POST** /api/workflow/bulk/terminate | Terminate workflows execution

# **pause_workflow1**
> BulkResponse pause_workflow1(body)

Pause the list of workflows

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowBulkResourceApi()
body = ['body_example'] # list[str] | 

try:
    # Pause the list of workflows
    api_response = api_instance.pause_workflow1(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowBulkResourceApi->pause_workflow1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)|  | 

### Return type

[**BulkResponse**](BulkResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restart1**
> BulkResponse restart1(body, use_latest_definitions=use_latest_definitions)

Restart the list of completed workflow

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowBulkResourceApi()
body = ['body_example'] # list[str] | 
use_latest_definitions = false # bool |  (optional) (default to false)

try:
    # Restart the list of completed workflow
    api_response = api_instance.restart1(body, use_latest_definitions=use_latest_definitions)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowBulkResourceApi->restart1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)|  | 
 **use_latest_definitions** | **bool**|  | [optional] [default to false]

### Return type

[**BulkResponse**](BulkResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_workflow1**
> BulkResponse resume_workflow1(body)

Resume the list of workflows

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowBulkResourceApi()
body = ['body_example'] # list[str] | 

try:
    # Resume the list of workflows
    api_response = api_instance.resume_workflow1(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowBulkResourceApi->resume_workflow1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)|  | 

### Return type

[**BulkResponse**](BulkResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retry1**
> BulkResponse retry1(body)

Retry the last failed task for each workflow from the list

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowBulkResourceApi()
body = ['body_example'] # list[str] | 

try:
    # Retry the last failed task for each workflow from the list
    api_response = api_instance.retry1(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowBulkResourceApi->retry1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)|  | 

### Return type

[**BulkResponse**](BulkResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **terminate**
> BulkResponse terminate(body, reason=reason)

Terminate workflows execution

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowBulkResourceApi()
body = ['body_example'] # list[str] | 
reason = 'reason_example' # str |  (optional)

try:
    # Terminate workflows execution
    api_response = api_instance.terminate(body, reason=reason)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowBulkResourceApi->terminate: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)|  | 
 **reason** | **str**|  | [optional] 

### Return type

[**BulkResponse**](BulkResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

