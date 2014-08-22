import json

from django_hstore_mixin.serializers import toJson


class JsonDict(dict):
    """ A dict-like object where all values are serialized to and from
    JSON upon setting and getting, allowing it to be stored in and
    retrieved from Hstore field while maintaining original type. """
    def __init__(self, data, modelInstance, *args, **kwargs):
        self._modelInstance = modelInstance
        data = data or {}  # Avoid data being NoneType
        super(self.__class__, self).__init__(data, *args, **kwargs)

    def __setitem__(self, k, v):
        # Serialize value being set
        super(self.__class__, self).__setitem__(k, toJson(v))

        # You can't use __setitem__ on a @property (ie. "e.data['foo'] = 1"
        # will return e._data as an object which then gets updated, but those
        # updates won't # make their way back to the db).  As such, we must
        # update the db field hiding behind the property manually.
        self._modelInstance._data = self.copy()

    def __getitem__(self, key):
        # Deserialize on 'get'
        return json.loads(super(self.__class__, self).__getitem__(key))

    def __getattr__(self, key):
        # Deserialize on 'get'
        return json.loads(super(self.__class__, self).__getattr__(key))

    def __repr__(self):
        # Deserialize values for reproduction
        return repr({k: v for k, v in self.items()})

    def __lt__(self, other):
        return {k: v for k, v in self.items()} < other

    def __le__(self, other):
        return {k: v for k, v in self.items()} <= other

    def __eq__(self, other):
        return {k: v for k, v in self.items()} == other

    def __ne__(self, other):
        return {k: v for k, v in self.items()} != other

    def __gt__(self, other):
        return {k: v for k, v in self.items()} > other

    def __ge__(self, other):
        return {k: v for k, v in self.items()} <= other

    def get(self, key, default=None):
        value = super(self.__class__, self).get(key, default)

        # Only deserialize if value was pulled from dict
        if value and value != default:
            value = json.loads(value)
        return value

    def items(self):
        return [(k, json.loads(v)) for k, v in super(self.__class__, self).items()]
