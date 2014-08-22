import datetime
import json


def toJson(d):
    """ Serialize data into JSON format """
    return (
        json.dumps(d.isoformat()) if isinstance(d, datetime.datetime) else
        json.dumps(d)
    )