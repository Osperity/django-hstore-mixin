# Django Hstore Mixin

_Note: This is called `Hstore Mixin` but really it's a base model_

Mixin to allow usage of Django Hstore whilst maintaining common Python
data types.

Note: Datetime objects will be serialized to ISO Format upon entrance
into DB but will not be deserialized upon retrieval.


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
