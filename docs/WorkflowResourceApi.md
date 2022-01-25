# swagger_client.WorkflowResourceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**decide**](WorkflowResourceApi.md#decide) | **PUT** /api/workflow/decide/{workflowId} | Starts the decision task for a workflow
[**delete**](WorkflowResourceApi.md#delete) | **DELETE** /api/workflow/{workflowId}/remove | Removes the workflow from the system
[**get_execution_status**](WorkflowResourceApi.md#get_execution_status) | **GET** /api/workflow/{workflowId} | Gets the workflow by workflow id
[**get_external_storage_location**](WorkflowResourceApi.md#get_external_storage_location) | **GET** /api/workflow/externalstoragelocation | Get the uri and path of the external storage where the workflow payload is to be stored
[**get_running_workflow**](WorkflowResourceApi.md#get_running_workflow) | **GET** /api/workflow/running/{name} | Retrieve all the running workflows
[**get_workflows**](WorkflowResourceApi.md#get_workflows) | **POST** /api/workflow/{name}/correlated | Lists workflows for the given correlation id list
[**get_workflows1**](WorkflowResourceApi.md#get_workflows1) | **GET** /api/workflow/{name}/correlated/{correlationId} | Lists workflows for the given correlation id
[**pause_workflow**](WorkflowResourceApi.md#pause_workflow) | **PUT** /api/workflow/{workflowId}/pause | Pauses the workflow
[**rerun**](WorkflowResourceApi.md#rerun) | **POST** /api/workflow/{workflowId}/rerun | Reruns the workflow from a specific task
[**reset_workflow**](WorkflowResourceApi.md#reset_workflow) | **POST** /api/workflow/{workflowId}/resetcallbacks | Resets callback times of all non-terminal SIMPLE tasks to 0
[**restart**](WorkflowResourceApi.md#restart) | **POST** /api/workflow/{workflowId}/restart | Restarts a completed workflow
[**resume_workflow**](WorkflowResourceApi.md#resume_workflow) | **PUT** /api/workflow/{workflowId}/resume | Resumes the workflow
[**retry**](WorkflowResourceApi.md#retry) | **POST** /api/workflow/{workflowId}/retry | Retries the last failed task
[**search**](WorkflowResourceApi.md#search) | **GET** /api/workflow/search | Search for workflows based on payload and other parameters
[**search_v2**](WorkflowResourceApi.md#search_v2) | **GET** /api/workflow/search-v2 | Search for workflows based on payload and other parameters
[**search_workflows_by_tasks**](WorkflowResourceApi.md#search_workflows_by_tasks) | **GET** /api/workflow/search-by-tasks | Search for workflows based on task parameters
[**search_workflows_by_tasks_v2**](WorkflowResourceApi.md#search_workflows_by_tasks_v2) | **GET** /api/workflow/search-by-tasks-v2 | Search for workflows based on task parameters
[**skip_task_from_workflow**](WorkflowResourceApi.md#skip_task_from_workflow) | **PUT** /api/workflow/{workflowId}/skiptask/{taskReferenceName} | Skips a given task from a current running workflow
[**start_workflow**](WorkflowResourceApi.md#start_workflow) | **POST** /api/workflow/{name} | Start a new workflow. Returns the ID of the workflow instance that can be later used for tracking
[**start_workflow1**](WorkflowResourceApi.md#start_workflow1) | **POST** /api/workflow | Start a new workflow with StartWorkflowRequest, which allows task to be executed in a domain
[**terminate1**](WorkflowResourceApi.md#terminate1) | **DELETE** /api/workflow/{workflowId} | Terminate workflow execution

# **decide**
> decide(workflow_id)

Starts the decision task for a workflow

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 

try:
    # Starts the decision task for a workflow
    api_instance.decide(workflow_id)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->decide: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete**
> delete(workflow_id, archive_workflow=archive_workflow)

Removes the workflow from the system

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 
archive_workflow = true # bool |  (optional) (default to true)

try:
    # Removes the workflow from the system
    api_instance.delete(workflow_id, archive_workflow=archive_workflow)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 
 **archive_workflow** | **bool**|  | [optional] [default to true]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_execution_status**
> Workflow get_execution_status(workflow_id, include_tasks=include_tasks)

Gets the workflow by workflow id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 
include_tasks = true # bool |  (optional) (default to true)

try:
    # Gets the workflow by workflow id
    api_response = api_instance.get_execution_status(workflow_id, include_tasks=include_tasks)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->get_execution_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 
 **include_tasks** | **bool**|  | [optional] [default to true]

### Return type

[**Workflow**](Workflow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_external_storage_location**
> ExternalStorageLocation get_external_storage_location(path, operation, payload_type)

Get the uri and path of the external storage where the workflow payload is to be stored

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
path = 'path_example' # str | 
operation = 'operation_example' # str | 
payload_type = 'payload_type_example' # str | 

try:
    # Get the uri and path of the external storage where the workflow payload is to be stored
    api_response = api_instance.get_external_storage_location(path, operation, payload_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->get_external_storage_location: %s\n" % e)
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

# **get_running_workflow**
> list[str] get_running_workflow(name, version=version, start_time=start_time, end_time=end_time)

Retrieve all the running workflows

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
name = 'name_example' # str | 
version = 1 # int |  (optional) (default to 1)
start_time = 789 # int |  (optional)
end_time = 789 # int |  (optional)

try:
    # Retrieve all the running workflows
    api_response = api_instance.get_running_workflow(name, version=version, start_time=start_time, end_time=end_time)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->get_running_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **version** | **int**|  | [optional] [default to 1]
 **start_time** | **int**|  | [optional] 
 **end_time** | **int**|  | [optional] 

### Return type

**list[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workflows**
> dict(str, list[Workflow]) get_workflows(body, name, include_closed=include_closed, include_tasks=include_tasks)

Lists workflows for the given correlation id list

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
body = ['body_example'] # list[str] | 
name = 'name_example' # str | 
include_closed = false # bool |  (optional) (default to false)
include_tasks = false # bool |  (optional) (default to false)

try:
    # Lists workflows for the given correlation id list
    api_response = api_instance.get_workflows(body, name, include_closed=include_closed, include_tasks=include_tasks)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->get_workflows: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[str]**](str.md)|  | 
 **name** | **str**|  | 
 **include_closed** | **bool**|  | [optional] [default to false]
 **include_tasks** | **bool**|  | [optional] [default to false]

### Return type

**dict(str, list[Workflow])**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workflows1**
> list[Workflow] get_workflows1(name, correlation_id, include_closed=include_closed, include_tasks=include_tasks)

Lists workflows for the given correlation id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
name = 'name_example' # str | 
correlation_id = 'correlation_id_example' # str | 
include_closed = false # bool |  (optional) (default to false)
include_tasks = false # bool |  (optional) (default to false)

try:
    # Lists workflows for the given correlation id
    api_response = api_instance.get_workflows1(name, correlation_id, include_closed=include_closed, include_tasks=include_tasks)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->get_workflows1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **correlation_id** | **str**|  | 
 **include_closed** | **bool**|  | [optional] [default to false]
 **include_tasks** | **bool**|  | [optional] [default to false]

### Return type

[**list[Workflow]**](Workflow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pause_workflow**
> pause_workflow(workflow_id)

Pauses the workflow

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 

try:
    # Pauses the workflow
    api_instance.pause_workflow(workflow_id)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->pause_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rerun**
> str rerun(body, workflow_id)

Reruns the workflow from a specific task

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
body = swagger_client.RerunWorkflowRequest() # RerunWorkflowRequest | 
workflow_id = 'workflow_id_example' # str | 

try:
    # Reruns the workflow from a specific task
    api_response = api_instance.rerun(body, workflow_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->rerun: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RerunWorkflowRequest**](RerunWorkflowRequest.md)|  | 
 **workflow_id** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_workflow**
> reset_workflow(workflow_id)

Resets callback times of all non-terminal SIMPLE tasks to 0

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 

try:
    # Resets callback times of all non-terminal SIMPLE tasks to 0
    api_instance.reset_workflow(workflow_id)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->reset_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **restart**
> restart(workflow_id, use_latest_definitions=use_latest_definitions)

Restarts a completed workflow

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 
use_latest_definitions = false # bool |  (optional) (default to false)

try:
    # Restarts a completed workflow
    api_instance.restart(workflow_id, use_latest_definitions=use_latest_definitions)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->restart: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 
 **use_latest_definitions** | **bool**|  | [optional] [default to false]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resume_workflow**
> resume_workflow(workflow_id)

Resumes the workflow

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 

try:
    # Resumes the workflow
    api_instance.resume_workflow(workflow_id)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->resume_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retry**
> retry(workflow_id, resume_subworkflow_tasks=resume_subworkflow_tasks)

Retries the last failed task

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 
resume_subworkflow_tasks = false # bool |  (optional) (default to false)

try:
    # Retries the last failed task
    api_instance.retry(workflow_id, resume_subworkflow_tasks=resume_subworkflow_tasks)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->retry: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 
 **resume_subworkflow_tasks** | **bool**|  | [optional] [default to false]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search**
> SearchResultWorkflowSummary search(start=start, size=size, sort=sort, free_text=free_text, query=query)

Search for workflows based on payload and other parameters

use sort options as sort=<field>:ASC|DESC e.g. sort=name&sort=workflowId:DESC. If order is not specified, defaults to ASC.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
start = 0 # int |  (optional) (default to 0)
size = 100 # int |  (optional) (default to 100)
sort = 'sort_example' # str |  (optional)
free_text = '*' # str |  (optional) (default to *)
query = 'query_example' # str |  (optional)

try:
    # Search for workflows based on payload and other parameters
    api_response = api_instance.search(start=start, size=size, sort=sort, free_text=free_text, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->search: %s\n" % e)
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

[**SearchResultWorkflowSummary**](SearchResultWorkflowSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_v2**
> SearchResultWorkflow search_v2(start=start, size=size, sort=sort, free_text=free_text, query=query)

Search for workflows based on payload and other parameters

use sort options as sort=<field>:ASC|DESC e.g. sort=name&sort=workflowId:DESC. If order is not specified, defaults to ASC.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
start = 0 # int |  (optional) (default to 0)
size = 100 # int |  (optional) (default to 100)
sort = 'sort_example' # str |  (optional)
free_text = '*' # str |  (optional) (default to *)
query = 'query_example' # str |  (optional)

try:
    # Search for workflows based on payload and other parameters
    api_response = api_instance.search_v2(start=start, size=size, sort=sort, free_text=free_text, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->search_v2: %s\n" % e)
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

[**SearchResultWorkflow**](SearchResultWorkflow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_workflows_by_tasks**
> SearchResultWorkflowSummary search_workflows_by_tasks(start=start, size=size, sort=sort, free_text=free_text, query=query)

Search for workflows based on task parameters

use sort options as sort=<field>:ASC|DESC e.g. sort=name&sort=workflowId:DESC. If order is not specified, defaults to ASC

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
start = 0 # int |  (optional) (default to 0)
size = 100 # int |  (optional) (default to 100)
sort = 'sort_example' # str |  (optional)
free_text = '*' # str |  (optional) (default to *)
query = 'query_example' # str |  (optional)

try:
    # Search for workflows based on task parameters
    api_response = api_instance.search_workflows_by_tasks(start=start, size=size, sort=sort, free_text=free_text, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->search_workflows_by_tasks: %s\n" % e)
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

[**SearchResultWorkflowSummary**](SearchResultWorkflowSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_workflows_by_tasks_v2**
> SearchResultWorkflow search_workflows_by_tasks_v2(start=start, size=size, sort=sort, free_text=free_text, query=query)

Search for workflows based on task parameters

use sort options as sort=<field>:ASC|DESC e.g. sort=name&sort=workflowId:DESC. If order is not specified, defaults to ASC

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
start = 0 # int |  (optional) (default to 0)
size = 100 # int |  (optional) (default to 100)
sort = 'sort_example' # str |  (optional)
free_text = '*' # str |  (optional) (default to *)
query = 'query_example' # str |  (optional)

try:
    # Search for workflows based on task parameters
    api_response = api_instance.search_workflows_by_tasks_v2(start=start, size=size, sort=sort, free_text=free_text, query=query)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->search_workflows_by_tasks_v2: %s\n" % e)
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

[**SearchResultWorkflow**](SearchResultWorkflow.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **skip_task_from_workflow**
> skip_task_from_workflow(workflow_id, task_reference_name, skip_task_request)

Skips a given task from a current running workflow

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 
task_reference_name = 'task_reference_name_example' # str | 
skip_task_request = swagger_client.SkipTaskRequest() # SkipTaskRequest | 

try:
    # Skips a given task from a current running workflow
    api_instance.skip_task_from_workflow(workflow_id, task_reference_name, skip_task_request)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->skip_task_from_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 
 **task_reference_name** | **str**|  | 
 **skip_task_request** | [**SkipTaskRequest**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_workflow**
> str start_workflow(body, name, version=version, correlation_id=correlation_id, priority=priority)

Start a new workflow. Returns the ID of the workflow instance that can be later used for tracking

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
body = NULL # dict(str, object) | 
name = 'name_example' # str | 
version = 56 # int |  (optional)
correlation_id = 'correlation_id_example' # str |  (optional)
priority = 0 # int |  (optional) (default to 0)

try:
    # Start a new workflow. Returns the ID of the workflow instance that can be later used for tracking
    api_response = api_instance.start_workflow(body, name, version=version, correlation_id=correlation_id, priority=priority)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->start_workflow: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**dict(str, object)**](dict.md)|  | 
 **name** | **str**|  | 
 **version** | **int**|  | [optional] 
 **correlation_id** | **str**|  | [optional] 
 **priority** | **int**|  | [optional] [default to 0]

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_workflow1**
> str start_workflow1(body)

Start a new workflow with StartWorkflowRequest, which allows task to be executed in a domain

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
body = swagger_client.StartWorkflowRequest() # StartWorkflowRequest | 

try:
    # Start a new workflow with StartWorkflowRequest, which allows task to be executed in a domain
    api_response = api_instance.start_workflow1(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->start_workflow1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**StartWorkflowRequest**](StartWorkflowRequest.md)|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **terminate1**
> terminate1(workflow_id, reason=reason)

Terminate workflow execution

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.WorkflowResourceApi()
workflow_id = 'workflow_id_example' # str | 
reason = 'reason_example' # str |  (optional)

try:
    # Terminate workflow execution
    api_instance.terminate1(workflow_id, reason=reason)
except ApiException as e:
    print("Exception when calling WorkflowResourceApi->terminate1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workflow_id** | **str**|  | 
 **reason** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

