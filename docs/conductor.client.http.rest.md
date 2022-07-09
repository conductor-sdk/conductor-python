<!-- markdownlint-disable -->

<a href="../src/conductor/client/http/rest.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.http.rest`






---

<a href="../src/conductor/client/http/rest.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RESTResponse`




<a href="../src/conductor/client/http/rest.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(resp)
```








---

<a href="../src/conductor/client/http/rest.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getheader`

```python
getheader(name, default=None)
```

Returns a given response header. 

---

<a href="../src/conductor/client/http/rest.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getheaders`

```python
getheaders()
```

Returns a dictionary of the response headers. 


---

<a href="../src/conductor/client/http/rest.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RESTClientObject`




<a href="../src/conductor/client/http/rest.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(configuration, pools_size=4, maxsize=None)
```








---

<a href="../src/conductor/client/http/rest.py#L236"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `DELETE`

```python
DELETE(
    url,
    headers=None,
    query_params=None,
    body=None,
    _preload_content=True,
    _request_timeout=None
)
```





---

<a href="../src/conductor/client/http/rest.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `GET`

```python
GET(
    url,
    headers=None,
    query_params=None,
    _preload_content=True,
    _request_timeout=None
)
```





---

<a href="../src/conductor/client/http/rest.py#L218"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `HEAD`

```python
HEAD(
    url,
    headers=None,
    query_params=None,
    _preload_content=True,
    _request_timeout=None
)
```





---

<a href="../src/conductor/client/http/rest.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `OPTIONS`

```python
OPTIONS(
    url,
    headers=None,
    query_params=None,
    post_params=None,
    body=None,
    _preload_content=True,
    _request_timeout=None
)
```





---

<a href="../src/conductor/client/http/rest.py#L265"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PATCH`

```python
PATCH(
    url,
    headers=None,
    query_params=None,
    post_params=None,
    body=None,
    _preload_content=True,
    _request_timeout=None
)
```





---

<a href="../src/conductor/client/http/rest.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `POST`

```python
POST(
    url,
    headers=None,
    query_params=None,
    post_params=None,
    body=None,
    _preload_content=True,
    _request_timeout=None
)
```





---

<a href="../src/conductor/client/http/rest.py#L255"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PUT`

```python
PUT(
    url,
    headers=None,
    query_params=None,
    post_params=None,
    body=None,
    _preload_content=True,
    _request_timeout=None
)
```





---

<a href="../src/conductor/client/http/rest.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `request`

```python
request(
    method,
    url,
    query_params=None,
    headers=None,
    body=None,
    post_params=None,
    _preload_content=True,
    _request_timeout=None
)
```

Perform requests. 

:param method: http request method :param url: http request url :param query_params: query parameters in the url :param headers: http request headers :param body: request json body, for `application/json` :param post_params: request post parameters,  `application/x-www-form-urlencoded`  and `multipart/form-data` :param _preload_content: if False, the urllib3.HTTPResponse object will  be returned without reading/decoding response  data. Default is True. :param _request_timeout: timeout setting for this request. If one  number provided, it will be total request  timeout. It can also be a pair (tuple) of  (connection, read) timeouts. 


---

<a href="../src/conductor/client/http/rest.py#L276"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ApiException`




<a href="../src/conductor/client/http/rest.py#L278"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(status=None, reason=None, http_resp=None)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
