# swagger_client.MetadataResourceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create**](MetadataResourceApi.md#create) | **POST** /api/metadata/workflow | Create a new workflow definition
[**get**](MetadataResourceApi.md#get) | **GET** /api/metadata/workflow/{name} | Retrieves workflow definition along with blueprint
[**get_all**](MetadataResourceApi.md#get_all) | **GET** /api/metadata/workflow | Retrieves all workflow definition along with blueprint
[**get_task_def**](MetadataResourceApi.md#get_task_def) | **GET** /api/metadata/taskdefs/{tasktype} | Gets the task definition
[**get_task_defs**](MetadataResourceApi.md#get_task_defs) | **GET** /api/metadata/taskdefs | Gets all task definition
[**register_task_def**](MetadataResourceApi.md#register_task_def) | **PUT** /api/metadata/taskdefs | Update an existing task
[**register_task_def1**](MetadataResourceApi.md#register_task_def1) | **POST** /api/metadata/taskdefs | Create new task definition(s)
[**unregister_task_def**](MetadataResourceApi.md#unregister_task_def) | **DELETE** /api/metadata/taskdefs/{tasktype} | Remove a task definition
[**unregister_workflow_def**](MetadataResourceApi.md#unregister_workflow_def) | **DELETE** /api/metadata/workflow/{name}/{version} | Removes workflow definition. It does not remove workflows associated with the definition.
[**update**](MetadataResourceApi.md#update) | **PUT** /api/metadata/workflow | Create or update workflow definition

# **create**
> create(body)

Create a new workflow definition

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()
body = swagger_client.WorkflowDef() # WorkflowDef | 

try:
    # Create a new workflow definition
    api_instance.create(body)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WorkflowDef**](WorkflowDef.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get**
> WorkflowDef get(name, version=version)

Retrieves workflow definition along with blueprint

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()
name = 'name_example' # str | 
version = 56 # int |  (optional)

try:
    # Retrieves workflow definition along with blueprint
    api_response = api_instance.get(name, version=version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **version** | **int**|  | [optional] 

### Return type

[**WorkflowDef**](WorkflowDef.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all**
> list[WorkflowDef] get_all()

Retrieves all workflow definition along with blueprint

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()

try:
    # Retrieves all workflow definition along with blueprint
    api_response = api_instance.get_all()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->get_all: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[WorkflowDef]**](WorkflowDef.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_task_def**
> TaskDef get_task_def(tasktype)

Gets the task definition

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()
tasktype = 'tasktype_example' # str | 

try:
    # Gets the task definition
    api_response = api_instance.get_task_def(tasktype)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->get_task_def: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tasktype** | **str**|  | 

### Return type

[**TaskDef**](TaskDef.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_task_defs**
> list[TaskDef] get_task_defs()

Gets all task definition

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()

try:
    # Gets all task definition
    api_response = api_instance.get_task_defs()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->get_task_defs: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[TaskDef]**](TaskDef.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_task_def**
> register_task_def(body)

Update an existing task

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()
body = swagger_client.TaskDef() # TaskDef | 

try:
    # Update an existing task
    api_instance.register_task_def(body)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->register_task_def: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskDef**](TaskDef.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_task_def1**
> register_task_def1(body)

Create new task definition(s)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()
body = [swagger_client.TaskDef()] # list[TaskDef] | 

try:
    # Create new task definition(s)
    api_instance.register_task_def1(body)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->register_task_def1: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[TaskDef]**](TaskDef.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unregister_task_def**
> unregister_task_def(tasktype)

Remove a task definition

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()
tasktype = 'tasktype_example' # str | 

try:
    # Remove a task definition
    api_instance.unregister_task_def(tasktype)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->unregister_task_def: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tasktype** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unregister_workflow_def**
> unregister_workflow_def(name, version)

Removes workflow definition. It does not remove workflows associated with the definition.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()
name = 'name_example' # str | 
version = 56 # int | 

try:
    # Removes workflow definition. It does not remove workflows associated with the definition.
    api_instance.unregister_workflow_def(name, version)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->unregister_workflow_def: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **version** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> update(body)

Create or update workflow definition

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.MetadataResourceApi()
body = [swagger_client.WorkflowDef()] # list[WorkflowDef] | 

try:
    # Create or update workflow definition
    api_instance.update(body)
except ApiException as e:
    print("Exception when calling MetadataResourceApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**list[WorkflowDef]**](WorkflowDef.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

