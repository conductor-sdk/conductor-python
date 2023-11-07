from conductor.client.http.rest import ApiException
import json
            
def api_exception_handler(function):
    def inner_function(*args, **kwargs):
        resp = None
        
        try:
            resp = function(*args, **kwargs)
        except ApiException as e:
            try:
                error = json.loads(e.body)
                resp = {
                    "error": {
                        "status": error['status'],
                        "message": error['message']
                    }
                }
            except ValueError:
                resp = { "error": e.body }

        return resp

    return inner_function

def for_all_methods(decorator, exclude=[]):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and attr not in exclude:
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate