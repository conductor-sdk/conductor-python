# swagger_client.AdminResourceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_config**](AdminResourceApi.md#get_all_config) | **GET** /api/admin/config | Get all the configuration parameters
[**get_event_queues**](AdminResourceApi.md#get_event_queues) | **GET** /api/admin/queues | Get registered queues
[**requeue_sweep**](AdminResourceApi.md#requeue_sweep) | **POST** /api/admin/sweep/requeue/{workflowId} | Queue up all the running workflows for sweep
[**verify_and_repair_workflow_consistency**](AdminResourceApi.md#verify_and_repair_workflow_consistency) | **POST** /api/admin/consistency/verifyAndRepair/{workflowId} | Verify and repair workflow consistency
[**view**](AdminResourceApi.md#view) | **GET** /api/admin/task/{tasktype} | Get the list of pending tasks for a given task type

# **get_all_config**
> dict(str, object) get_all_config()

Get all the configuration parameters

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AdminResourceApi()

try:
    # Get all the configuration parameters
    api_response = api_instance.get_all_config()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminResourceApi->get_all_config: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**dict(str, object)**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_event_queues**
> dict(str, object) get_event_queues(verbose=verbose)

Get registered queues

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AdminResourceApi()
verbose = false # bool |  (optional) (default to false)

try:
    # Get registered queues
    api_response = api_instance.get_event_queues(verbose=verbose)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminResourceApi->get_event_queues: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **verbose** | **bool**|  | [optional] [default to false]

### Return type

**dict(str, object)**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **requeue_sweep**
> str requeue_sweep(workflow_id)

Queue up all the running workflows for sweep

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AdminResourceApi()
workflow_id = 'workflow_id_example' # str | 

try:
    # Queue up all the running workflows for sweep
    api_response = api_instance.requeue_sweep(workflow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminResourceApi->requeue_sweep: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **verify_and_repair_workflow_consistency**
> str verify_and_repair_workflow_consistency(workflow_id)

Verify and repair workflow consistency

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AdminResourceApi()
workflow_id = 'workflow_id_example' # str | 

try:
    # Verify and repair workflow consistency
    api_response = api_instance.verify_and_repair_workflow_consistency(workflow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminResourceApi->verify_and_repair_workflow_consistency: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **view**
> list[Task] view(tasktype, start=start, count=count)

Get the list of pending tasks for a given task type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AdminResourceApi()
tasktype = 'tasktype_example' # str | 
start = 0 # int |  (optional) (default to 0)
count = 100 # int |  (optional) (default to 100)

try:
    # Get the list of pending tasks for a given task type
    api_response = api_instance.view(tasktype, start=start, count=count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminResourceApi->view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tasktype** | **str**|  | 
 **start** | **int**|  | [optional] [default to 0]
 **count** | **int**|  | [optional] [default to 100]

### Return type

[**list[Task]**](Task.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

