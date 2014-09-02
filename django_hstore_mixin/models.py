import datetime
import json

from django.core.exceptions import ValidationError
from django.db import models
from django_hstore import hstore

from django_hstore_mixin.data_types import JsonDict
from django_hstore_mixin.serializers import toJson


class HstoreMixin(models.Model):
    """ Data field to be added to model to enable Hstore field. Actual
    hstore field hidden with underscore, property field serializes and
    deserializes data upon setting/getting. """
    _data = hstore.DictionaryField(
        'KeyValueStore',
        db_index=True, null=True, blank=True
    )
    objects = hstore.HStoreManager()

    class Meta:
        abstract = True

    def clean(self):
        """ Ensure that all Hstore data is stored as valid JSON.
        NOTE: By default, this is not called automatically when you call
        save() method. """
        for key, value in self._data.items():
            try:
                json.loads(value)
            except ValueError:
                msg = "The value of key \"%s\" does not appear to be valid JSON: %s. " % (key, value)
                msg += "Hstore values must be stored as JSON.  Maybe you meant to use %s?" % json.dumps(value)
                raise ValidationError(msg)
        return super(HstoreMixin, self).clean()

    @property
    def data(self):
        """ Decode data from JSON """
        return JsonDict(self._data, modelInstance=self)
    @data.setter
    def data(self, value):
        """ Encode data to JSON """
        if not self._data:
            self._data = {k: toJson(v) for k, v in value.items()}
        else:
            self._data = JsonDict(value, modelInstance=self)
