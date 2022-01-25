# swagger_client.EventResourceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_event_handler**](EventResourceApi.md#add_event_handler) | **POST** /api/event | Add a new event handler.
[**get_event_handlers**](EventResourceApi.md#get_event_handlers) | **GET** /api/event | Get all the event handlers
[**get_event_handlers_for_event**](EventResourceApi.md#get_event_handlers_for_event) | **GET** /api/event/{event} | Get event handlers for a given event
[**remove_event_handler_status**](EventResourceApi.md#remove_event_handler_status) | **DELETE** /api/event/{name} | Remove an event handler
[**update_event_handler**](EventResourceApi.md#update_event_handler) | **PUT** /api/event | Update an existing event handler.

# **add_event_handler**
> add_event_handler(body)

Add a new event handler.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventResourceApi()
body = swagger_client.EventHandler() # EventHandler | 

try:
    # Add a new event handler.
    api_instance.add_event_handler(body)
except ApiException as e:
    print("Exception when calling EventResourceApi->add_event_handler: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EventHandler**](EventHandler.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_event_handlers**
> list[EventHandler] get_event_handlers()

Get all the event handlers

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventResourceApi()

try:
    # Get all the event handlers
    api_response = api_instance.get_event_handlers()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventResourceApi->get_event_handlers: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[EventHandler]**](EventHandler.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_event_handlers_for_event**
> list[EventHandler] get_event_handlers_for_event(event, active_only=active_only)

Get event handlers for a given event

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventResourceApi()
event = 'event_example' # str | 
active_only = true # bool |  (optional) (default to true)

try:
    # Get event handlers for a given event
    api_response = api_instance.get_event_handlers_for_event(event, active_only=active_only)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventResourceApi->get_event_handlers_for_event: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **event** | **str**|  | 
 **active_only** | **bool**|  | [optional] [default to true]

### Return type

[**list[EventHandler]**](EventHandler.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_event_handler_status**
> remove_event_handler_status(name)

Remove an event handler

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventResourceApi()
name = 'name_example' # str | 

try:
    # Remove an event handler
    api_instance.remove_event_handler_status(name)
except ApiException as e:
    print("Exception when calling EventResourceApi->remove_event_handler_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_event_handler**
> update_event_handler(body)

Update an existing event handler.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventResourceApi()
body = swagger_client.EventHandler() # EventHandler | 

try:
    # Update an existing event handler.
    api_instance.update_event_handler(body)
except ApiException as e:
    print("Exception when calling EventResourceApi->update_event_handler: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EventHandler**](EventHandler.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

