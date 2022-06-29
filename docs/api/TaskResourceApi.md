# swagger_client.TaskResourceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**all**](TaskResourceApi.md#all) | **GET** /api/tasks/queue/all | Get the details about each queue
[**all_verbose**](TaskResourceApi.md#all_verbose) | **GET** /api/tasks/queue/all/verbose | Get the details about each queue
[**batch_poll**](TaskResourceApi.md#batch_poll) | **GET** /api/tasks/poll/batch/{tasktype} | Batch poll for a task of a certain type
[**get_all_poll_data**](TaskResourceApi.md#get_all_poll_data) | **GET** /api/tasks/queue/polldata/all | Get the last poll data for all task types
[**get_external_storage_location1**](TaskResourceApi.md#get_external_storage_location1) | **GET** /api/tasks/externalstoragelocation | Get the external uri where the task payload is to be stored
[**get_poll_data**](TaskResourceApi.md#get_poll_data) | **GET** /api/tasks/queue/polldata | Get the last poll data for a given task type
[**get_task**](TaskResourceApi.md#get_task) | **GET** /api/tasks/{taskId} | Get task by Id
[**get_task_logs**](TaskResourceApi.md#get_task_logs) | **GET** /api/tasks/{taskId}/log | Get Task Execution Logs
[**log**](TaskResourceApi.md#log) | **POST** /api/tasks/{taskId}/log | Log Task Execution Details
[**poll**](TaskResourceApi.md#poll) | **GET** /api/tasks/poll/{tasktype} | Poll for a task of a certain type
[**requeue_pending_task**](TaskResourceApi.md#requeue_pending_task) | **POST** /api/tasks/queue/requeue/{taskType} | Requeue pending tasks
[**search1**](TaskResourceApi.md#search1) | **GET** /api/tasks/search | Search for tasks based in payload and other parameters
[**search_v21**](TaskResourceApi.md#search_v21) | **GET** /api/tasks/search-v2 | Search for tasks based in payload and other parameters
[**size**](TaskResourceApi.md#size) | **GET** /api/tasks/queue/sizes | Get Task type queue sizes
[**update_task**](TaskResourceApi.md#update_task) | **POST** /api/tasks | Update a task

# **all**
> dict(str, int) all()

Get the details about each queue

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()

try:
    # Get the details about each queue
    api_response = api_instance.all()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->all: %s\n" % e)
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

# **all_verbose**
> dict(str, dict(str, dict(str, int))) all_verbose()

Get the details about each queue

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()

try:
    # Get the details about each queue
    api_response = api_instance.all_verbose()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->all_verbose: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**dict(str, dict(str, dict(str, int)))**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **batch_poll**
> list[Task] batch_poll(tasktype, workerid=workerid, domain=domain, count=count, timeout=timeout)

Batch poll for a task of a certain type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
tasktype = 'tasktype_example' # str | 
workerid = 'workerid_example' # str |  (optional)
domain = 'domain_example' # str |  (optional)
count = 1 # int |  (optional) (default to 1)
timeout = 100 # int |  (optional) (default to 100)

try:
    # Batch poll for a task of a certain type
    api_response = api_instance.batch_poll(tasktype, workerid=workerid, domain=domain, count=count, timeout=timeout)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->batch_poll: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tasktype** | **str**|  | 
 **workerid** | **str**|  | [optional] 
 **domain** | **str**|  | [optional] 
 **count** | **int**|  | [optional] [default to 1]
 **timeout** | **int**|  | [optional] [default to 100]

### Return type

[**list[Task]**](Task.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_poll_data**
> list[PollData] get_all_poll_data()

Get the last poll data for all task types

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()

try:
    # Get the last poll data for all task types
    api_response = api_instance.get_all_poll_data()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->get_all_poll_data: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[PollData]**](PollData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_external_storage_location1**
> ExternalStorageLocation get_external_storage_location1(path, operation, payload_type)

Get the external uri where the task payload is to be stored

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
path = 'path_example' # str | 
operation = 'operation_example' # str | 
payload_type = 'payload_type_example' # str | 

try:
    # Get the external uri where the task payload is to be stored
    api_response = api_instance.get_external_storage_location1(path, operation, payload_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->get_external_storage_location1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **path** | **str**|  | 
 **operation** | **str**|  | 
 **payload_type** | **str**|  | 

### Return type

[**ExternalStorageLocation**](ExternalStorageLocation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_poll_data**
> list[PollData] get_poll_data(task_type)

Get the last poll data for a given task type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
task_type = 'task_type_example' # str | 

try:
    # Get the last poll data for a given task type
    api_response = api_instance.get_poll_data(task_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->get_poll_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_type** | **str**|  | 

### Return type

[**list[PollData]**](PollData.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_task**
> Task get_task(task_id)

Get task by Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
task_id = 'task_id_example' # str | 

try:
    # Get task by Id
    api_response = api_instance.get_task(task_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->get_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **str**|  | 

### Return type

[**Task**](Task.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_task_logs**
> list[TaskExecLog] get_task_logs(task_id)

Get Task Execution Logs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
task_id = 'task_id_example' # str | 

try:
    # Get Task Execution Logs
    api_response = api_instance.get_task_logs(task_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->get_task_logs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | **str**|  | 

### Return type

[**list[TaskExecLog]**](TaskExecLog.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **log**
> log(body, task_id)

Log Task Execution Details

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
body = 'body_example' # str | 
task_id = 'task_id_example' # str | 

try:
    # Log Task Execution Details
    api_instance.log(body, task_id)
except ApiException as e:
    print("Exception when calling TaskResourceApi->log: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**str**](str.md)|  | 
 **task_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **poll**
> Task poll(tasktype, workerid=workerid, domain=domain)

Poll for a task of a certain type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
tasktype = 'tasktype_example' # str | 
workerid = 'workerid_example' # str |  (optional)
domain = 'domain_example' # str |  (optional)

try:
    # Poll for a task of a certain type
    api_response = api_instance.poll(tasktype, workerid=workerid, domain=domain)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->poll: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tasktype** | **str**|  | 
 **workerid** | **str**|  | [optional] 
 **domain** | **str**|  | [optional] 

### Return type

[**Task**](Task.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **requeue_pending_task**
> str requeue_pending_task(task_type)

Requeue pending tasks

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
task_type = 'task_type_example' # str | 

try:
    # Requeue pending tasks
    api_response = api_instance.requeue_pending_task(task_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->requeue_pending_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_type** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search1**
> SearchResultTaskSummary search1(start=start, size=size, sort=sort, free_text=free_text, query=query)

Search for tasks based in payload and other parameters

use sort options as sort=<field>:ASC|DESC e.g. sort=name&sort=workflowId:DESC. If order is not specified, defaults to ASC

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
start = 0 # int |  (optional) (default to 0)
size = 100 # int |  (optional) (default to 100)
sort = 'sort_example' # str |  (optional)
free_text = '*' # str |  (optional) (default to *)
query = 'query_example' # str |  (optional)

try:
    # Search for tasks based in payload and other parameters
    api_response = api_instance.search1(start=start, size=size, sort=sort, free_text=free_text, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->search1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start** | **int**|  | [optional] [default to 0]
 **size** | **int**|  | [optional] [default to 100]
 **sort** | **str**|  | [optional] 
 **free_text** | **str**|  | [optional] [default to *]
 **query** | **str**|  | [optional] 

### Return type

[**SearchResultTaskSummary**](SearchResultTaskSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_v21**
> SearchResultTask search_v21(start=start, size=size, sort=sort, free_text=free_text, query=query)

Search for tasks based in payload and other parameters

use sort options as sort=<field>:ASC|DESC e.g. sort=name&sort=workflowId:DESC. If order is not specified, defaults to ASC

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
start = 0 # int |  (optional) (default to 0)
size = 100 # int |  (optional) (default to 100)
sort = 'sort_example' # str |  (optional)
free_text = '*' # str |  (optional) (default to *)
query = 'query_example' # str |  (optional)

try:
    # Search for tasks based in payload and other parameters
    api_response = api_instance.search_v21(start=start, size=size, sort=sort, free_text=free_text, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->search_v21: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start** | **int**|  | [optional] [default to 0]
 **size** | **int**|  | [optional] [default to 100]
 **sort** | **str**|  | [optional] 
 **free_text** | **str**|  | [optional] [default to *]
 **query** | **str**|  | [optional] 

### Return type

[**SearchResultTask**](SearchResultTask.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **size**
> dict(str, int) size(task_type=task_type)

Get Task type queue sizes

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
task_type = ['task_type_example'] # list[str] |  (optional)

try:
    # Get Task type queue sizes
    api_response = api_instance.size(task_type=task_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->size: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_type** | [**list[str]**](str.md)|  | [optional] 

### Return type

**dict(str, int)**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_task**
> str update_task(body)

Update a task

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.TaskResourceApi()
body = swagger_client.TaskResult() # TaskResult | 

try:
    # Update a task
    api_response = api_instance.update_task(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TaskResourceApi->update_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskResult**](TaskResult.md)|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

