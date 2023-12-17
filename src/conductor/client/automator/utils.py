import dataclasses
import datetime
import inspect
import logging
import typing
from typing import List

from dacite import from_dict
from requests.structures import CaseInsensitiveDict

from conductor.client.configuration.configuration import Configuration

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)

simple_types = {
    int, float, str, bool, datetime.date, datetime.datetime, object
}
dict_types = {
    dict, typing.Dict, CaseInsensitiveDict
}
collection_types = {
    list, List, typing.Set
}


def convert(cls: type, data: dict) -> object:
    if dataclasses.is_dataclass(cls):
        return from_dict(data_class=cls, data=data)

    if type(data) != dict:
        data = {}
    members = inspect.signature(cls.__init__).parameters
    kwargs = {}

    for member in members:
        if 'self' == member:
            continue
        typ = members[member].annotation
        generic_types = typing.get_args(members[member].annotation)

        if typ in simple_types:
            if member in data:
                kwargs[member] = data[member]
            else:
                kwargs[member] = members[member].default
        elif str(typ).startswith('typing.List[') or str(typ).startswith('typing.Set[') or str(typ).startswith('list['):
            values = []
            generic_type = object
            if len(generic_types) > 0:
                generic_type = generic_types[0]
            for val in data[member]:
                values.append(get_value(generic_type, val))
            kwargs[member] = values
        elif str(typ).startswith('dict[') or str(typ).startswith(
                'typing.Dict[') or str(typ).startswith('requests.structures.CaseInsensitiveDict[') or typ == dict or str(typ).startswith('OrderedDict['):
            values = {}
            generic_type = object
            if len(generic_types) > 1:
                generic_type = generic_types[1]
            for k in data[member]:
                v = data[member][k]
                values[k] = get_value(generic_type, v)
            kwargs[member] = values
        elif typ == inspect.Parameter.empty:
            if members[member].kind == inspect.Parameter.VAR_KEYWORD:
                if type(data) in dict_types:
                    kwargs.update(data)
                else:
                    kwargs.update(data[member])
            else:
                logger.info(f'setting value for {member} and data is {data} and kwargs is {kwargs}')
                kwargs[member] = data[member]
        else:
            kwargs[member] = convert(typ, data[member])

    return cls(**kwargs)


def get_value(typ: type, val: object) -> object:
    if typ in simple_types:
        return val
    elif str(typ).startswith('typing.List[') or str(typ).startswith('typing.Set[') or str(typ).startswith('list['):
        values = []
        for val in val:
            converted = get_value(type(val), val)
            values.append(converted)
        return values
    elif str(typ).startswith('dict[') or str(typ).startswith(
            'typing.Dict[') or str(typ).startswith('requests.structures.CaseInsensitiveDict[') or typ == dict:
        values = {}
        for k in val:
            v = val[k]
            values[k] = get_value(object, v)
        return values
    else:
        return convert(typ, val)