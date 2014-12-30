import datetime
import json


def serializeItem(d):
    """ Serialize single value into JSON format """
    return (
        json.dumps(d.isoformat()) if isinstance(d, datetime.datetime) else
        json.dumps(d)
    )

def serializeDict(d):
    """ Serialize dictionary's values into JSON format """
    return {k: serializeItem(v) for k, v in d.items()}
