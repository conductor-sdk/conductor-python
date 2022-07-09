<!-- markdownlint-disable -->

<a href="../src/conductor/client/configuration/configuration.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.configuration.configuration`






---

<a href="../src/conductor/client/configuration/configuration.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Configuration`




<a href="../src/conductor/client/configuration/configuration.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    base_url: str = 'http://localhost:8080',
    debug: bool = False,
    authentication_settings: AuthenticationSettings = None,
    server_api_url: str = None
)
```






---

#### <kbd>property</kbd> debug

Debug status 

:param value: The debug status, True or False. :type: bool 

---

#### <kbd>property</kbd> logger_format

The logger format. 

The logger_formatter will be updated when sets logger_format. 

:param value: The format string. :type: str 



---

<a href="../src/conductor/client/configuration/configuration.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `apply_logging_config`

```python
apply_logging_config()
```





---

<a href="../src/conductor/client/configuration/configuration.py#L112"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_logging_formatted_name`

```python
get_logging_formatted_name(name)
```





---

<a href="../src/conductor/client/configuration/configuration.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_token`

```python
update_token(token: str) → None
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
