from django_hstore_mixin.models import HstoreMixin

# determine if geodjango is in use
# GEODJANGO = settings.DATABASES['default']['ENGINE'] == 'django.contrib.gis.db.backends.postgis'


__all__ = [
    'TestModel',
]


class TestModel(HstoreMixin):
    pass
