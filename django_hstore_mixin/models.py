from django.core.exceptions import ValidationError
from django.db import models
from django_hstore import hstore

from .data_types import JsonDict


class HstoreMixin(models.Model):
    """ Data field to be added to model to enable Hstore field. Actual
    hstore field hidden with underscore, property field serializes and
    deserializes data upon setting/getting. """
    _data = hstore.DictionaryField(
        'KeyValueStore',
        db_index=True,
        default={},
        blank=True,
        null=True
    )
    objects = hstore.HStoreManager()

    class Meta:
        abstract = True

    def clean(self):
        """ Ensure that all Hstore data is stored as valid JSON.
        NOTE: By default, this is not called automatically when you call
        save() method. """
        if self._data:
            for key, value in self._data.items():
                try:
                    JsonDict.deserializeValue(value)
                except ValueError:
                    msg = "The value of key \"%s\" does not appear to be valid JSON: %s. " % (key, value)
                    msg += "Hstore values must be stored as JSON.  Maybe you meant to use %s?" % JsonDict.serializeValue(value)
                    raise ValidationError(msg)
        return super(HstoreMixin, self).clean()

    @property
    def data(self):
        """ Decode data from JSON """
        return JsonDict(self._data, modelInstance=self)
    @data.setter
    def data(self, value):
        """ Encode data to JSON """
        self._data = JsonDict.serializeDict(value) if value else {}
