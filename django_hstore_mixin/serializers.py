import datetime
import json


def serializeValue(v):
    """ Serialize single value into JSON format """
    return (
        json.dumps(v.isoformat()) if isinstance(v, datetime.datetime) else
        json.dumps(v)
    )

def serializeDict(d):
    """ Serialize dictionary's values into JSON format """
    return {k: serializeValue(v) for k, v in d.items()}

def deserializeValue(v):
    try:
        return json.loads(v)
    except ValueError:
        raise ValueError("No JSON object could be decoded from \"%s\"" % v)
