import json
from enum import Enum


class JSONYEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Enum):
            return o.value
        if hasattr(o, "__iter__"):
            return list(o)
        if hasattr(o, "__str__"):
            return str(o)
        return super().default(o)
