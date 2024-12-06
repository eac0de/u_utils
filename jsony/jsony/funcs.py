import json
from typing import Any

from .encoder import JSONYEncoder


def normalize(data: Any) -> Any:
    json_data = json.dumps(data, cls=JSONYEncoder)
    return json.loads(json_data)


def dumps(
    obj,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kw
) -> Any:
    return json.dumps(
        obj=obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=JSONYEncoder,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kw,
    )


def dump(
    obj,
    fp,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kw
) -> Any:
    return json.dump(
        obj=obj,
        fp=fp,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=JSONYEncoder,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kw,
    )
