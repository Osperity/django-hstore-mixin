# Django Hstore Mixin

Mixin to allow usage of `django-hstore` whilst maintaining common Python
data types.

## Introduction

This is an add-on for the [`django-hstore`](https://github.com/djangonauts/django-hstore) library.  While the `django-hstore` 
library does many amazing things, it suffers from the fact that does not maintain many datatypes (unless the newer `schema mode`
is used, which is somewhat of a manual process).  This is due to the fact that Postgresql can only store values as `String` objects.

To get around this limitation, the `django-hstore-mixin` creates a `property` on a model that acts as a proxy for the `django-hstore`
field.  Anything put into this field is serialized to JSON on input and deserialized from JSON on retrieval.

_Note: Datetime objects will be serialized to ISO Format upon entrance
into DB but will not be deserialized upon retrieval._

## Installation

1. Install `django-hstore` as per it's [installation instructions](http://djangonauts.github.io/django-hstore/#_install).

2. Install `django-hstore-mixin`:

    `-e git+git@bitbucket.org:ospreyinformatics/django-hstore-mixin.git@[VERSION_TAG]#egg=django_hstore_mixin`

3. That's about it, no need to touch your `INSTALLED_APPS`.  Just import and use the mixin as needed!

## Usage

To use the `django-hstore-mixin`, simply import the HstoreMixin and use it in a model's base.

    from django_hstore_mixin.models import HstoreMixin


    class ExampleModel(HstoreMixin):
        """
        A model with a Django Hstore object that retains data types.
        """
        name = models.CharField(max_length=128, null=True, blank=True)

Now, the model with have a dictionary-like `data` property and a hidden `_data` field, which is the actual `django-hstore` field.  
Anything written-to/read-from `data` will be serialized/deserialized to/from JSON and stored the `_data` field.  Additionally, data written to the
to `data` field will undergo some basic validation to ensure that it can be properly serialized to JSON.

    instance = ExampleModel.objects.create(
        data=dict(
            int=1,
            string='foo',
            date=datetime.datetime.now(),
            list=[1, 'two'],
            dict=dict(a=1)
        )
    )

    >>> instance.data.get('int')    # Still an int...
    1
    >>> instance.data.get('string') # Naturally, still a string...
    u'foo'
    >>> instance.data.get('list')   # Still a list...
    [1, u'two']
    >>> instance.data.get('dict')   # Still a dict...
    {u'a': 1}
    >>> instance.data.get('date')   # Oops, not a datetime. An isoformat datetime string...
    u'2014-10-14T19:54:39.248970'

    >>> instance.data               # Returned as a dict-like object
    {'date': u'2014-10-14T19:54:39.248970', 'int': 1, 'list': [1, u'two'], 'string': u'foo', 'dict': {u'a': 1}}
    >>> type(instance.data)         # Not actuall a dict
    <class 'django_hstore_mixin.data_types.JsonDict'>
    >>> isinstance(instance.data, dict)  # But an instance of a dict
    True


During all of this, you can view how the data is serialized by looking at the `_data` property...


    >>> instance._data.get('int')    # Stored as a JSON string of an int...
    '1'
    >>> instance._data.get('string') # Stored as a JSON string of a string...
    '"foo"'
    >>> instance._data.get('list')   # Stored as a JSON string of a list...
    '[1, "two"]'
    >>> instance._data.get('dict')   # Stored as a JSON string of a dict...
    '{"a": 1}'
    >>> instance._data.get('date')   # Stored as a JSON string of an isoformat datetime string...
    '"2014-10-14T19:54:39.248970"'

    >>> instance._data
    {'date': '"2014-10-14T19:54:39.248970"', 'int': '1', 'list': '[1, "two"]', 'string': '"foo"', 'dict': '{"a": 1}'}
    >>> type(instance._data)
    <class 'django_hstore.dict.HStoreDict'>

## Limitations

Currently, the `data` property name and `_data` field name is hardcoded.  Additionally, the `objects` 
manager is overwritten with the `hstore.HStoreManager()`.

## Running tests

Assuming one has the dependencies installed, and a *PostgreSQL 9.0+* server up and
running:

    python runtests.py

By default the tests run with the postgis backend.

If you want to run the tests with psycopg2 backend you can do:

    python runtests.py --settings=settings_psycopg

You might need to tweak the DB settings according to your DB configuration.

If you need to do so you can copy the file `local_settings.py.example` to `local_settings.py` and add
your database tweaks on it. `local_settings.py` will be automatically imported in `settings.py`.
The same applies for `local_settings_psycopg.py.example`, which will be imported in
`local_settings_psycopg.py`.

If after running this command you get an *error* saying:

    type "hstore" does not exist

Try this:

    psql template1 -c 'create extension hstore;'

More details here on link: http://clarkdave.net/2012/09/postgresql-error-type-hstore-does-not-exist/[PostgreSQL error type hstore does not exist].

## Contributions/Issues

The preferred way to make a contribution to the `django-hstore-mixin` is by forking the repo, making changes, and then opening a [Pull Request](pull-requests).

The preferred way to raise attention to a bug/issue is by opening an [Issue](issues).