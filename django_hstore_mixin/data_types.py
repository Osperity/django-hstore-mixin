from django_hstore_mixin.serializers import deserializeValue, serializeValue, serializeDict


__all__ = ('JsonDict',)


class JsonDict(dict):
    """ A dict-like object where all values are serialized to and from
    JSON upon setting and getting, allowing it to be stored in and
    retrieved from Hstore field while maintaining original type. """
    def __init__(self, data, modelInstance, datafield='_data', *args, **kwargs):
        self._modelInstance = modelInstance
        self._datafield = datafield
        data = data or {}  # Avoid data being NoneType
        super(JsonDict, self).__init__(data, *args, **kwargs)

    def __setitem__(self, k, v):
        # Serialize value being set
        super(JsonDict, self).__setitem__(k, serializeValue(v))

        # You can't use __setitem__ on a @property (ie. "e.data['foo'] = 1"
        # will return e._data as an object which then gets updated, but those
        # updates won't make their way back to the db).  As such, we must
        # update the db field hiding behind the property manually.
        self._apply_to_field(dict(self))

    def __getitem__(self, key):
        # Deserialize on 'get'
        return deserializeValue(super(JsonDict, self).__getitem__(key))

    def __getattr__(self, key):
        # Deserialize on 'get'
        return deserializeValue(super(JsonDict, self).__getattr__(key))

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

    def _apply_to_field(self, dictionary):
        """ Apply value to underlying hstore field """
        setattr(self._modelInstance, self._datafield, dictionary)

    def get(self, key, default=None):
        value = super(JsonDict, self).get(key, default)

        # Only deserialize if value was pulled from dict
        if value and value != default:
            value = deserializeValue(value)
        return value

    def items(self):
        return [(k, deserializeValue(v)) for k, v in super(JsonDict, self).items()]

    def iteritems(self):
        for (k, v) in super(JsonDict, self).iteritems():
            yield (k, deserializeValue(v))

    def itervalues(self):
        for v in super(JsonDict, self).itervalues():
            yield deserializeValue(v)

    def update(self, other):
        # This is pretty ugly.
        dict_self = dict(self)
        dict_self.update(serializeDict(other))
        self._apply_to_field(dict_self)

    @staticmethod
    def deserializeValue(value):
        """ Convenience method to provide interface to deserializeValue tooling """
        return deserializeValue(value)

    @staticmethod
    def serializeValue(value):
        """ Convenience method to provide interface to serializeValue tooling """
        return serializeValue(value)

    @staticmethod
    def serializeDict(dictionary):
        """ Convenience method to provide interface to serializeDict tooling """
        return serializeDict(dictionary)
