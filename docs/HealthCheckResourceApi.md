# swagger_client.HealthCheckResourceApi

All URIs are relative to *http://localhost:8080*

Method | HTTP request | Description
------------- | ------------- | -------------
[**do_check**](HealthCheckResourceApi.md#do_check) | **GET** /health | 

# **do_check**
> HealthCheckStatus do_check()



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.HealthCheckResourceApi()

try:
    api_response = api_instance.do_check()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HealthCheckResourceApi->do_check: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**HealthCheckStatus**](HealthCheckStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

