# -*- coding: utf-8 -*-
import datetime
import json

from django.core.exceptions import ValidationError
from django.forms.models import modelform_factory
from django.test import TestCase

from django_hstore_mixin_tests.models import TestModel


class TestHstoreMixin(TestCase):

    def setUp(self):
        self.now = datetime.datetime.now()
        self.instance = TestModel.objects.create(
            data=dict(
                int=1,
                string='foo',
                date=self.now,
                list=[1, 'two'],
                dict=dict(a=1)
            )
        )

    def test_setting(self):
        """ Ensure data is set/serialized properly """
        self.assertEqual(
            self.instance._data,
            {
                'date': json.dumps(self.now.isoformat()),
                'int': '1',
                'list': '[1, "two"]',
                'string': '"foo"',
                'dict': '{"a": 1}'
            }
        )

        self.instance.data['int'] = 3
        self.instance.save()
        self.assertEqual(self.instance._data['int'], '3')

        self.instance.data['list'] = [2, 'three']
        self.instance.save()
        self.assertEqual(self.instance._data['list'], '[2, "three"]')

        self.instance.data['string'] = 'Foo'
        self.instance.save()
        self.assertEqual(self.instance._data['string'], '"Foo"')

        self.instance.data['dict'] = dict(a=2)
        self.instance.save()
        self.assertEqual(self.instance._data['dict'], '{"a": 2}')

    def test_getting(self):
        """ Ensure data is retrieved/deserialized properly """
        self.assertEqual(
            self.instance.data,
            dict(int=1, string='foo', date=self.now.isoformat(), list=[1, 'two'], dict={'a': 1})
        )

        self.assertEqual(self.instance.data.get('int'), 1)
        self.assertEqual(self.instance.data.get('string'), 'foo')
        self.assertEqual(self.instance.data.get('date'), self.now.isoformat())
        self.assertEqual(self.instance.data.get('list'), [1, 'two'])
        self.assertEqual(self.instance.data.get('dict'), {'a': 1})
        self.assertEqual(self.instance.data.get('notThere'), None)
        self.assertEqual(self.instance.data.get('notThere', 'Nope'), 'Nope')

        self.assertEqual(self.instance.data['int'], 1)
        self.assertEqual(self.instance.data['string'], 'foo')
        self.assertEqual(self.instance.data['date'], self.now.isoformat())
        self.assertEqual(self.instance.data['list'], [1, 'two'])
        self.assertEqual(self.instance.data['dict'], {'a': 1})
        with self.assertRaises(KeyError):
            self.instance.data['notThere']

    def test_comparison(self):
        """ Ensure data is compares in a deserialized form """
        self.assertEqual(
            self.instance.data,
            dict(
                int=1,
                string='foo',
                date=self.now.isoformat(),
                list=[1, 'two'],
                dict={'a': 1}
            )
        )
        self.assertEqual(
            dict(
                int=1,
                string='foo',
                date=self.now.isoformat(),
                list=[1, 'two'],
                dict={'a': 1}
            ),
            self.instance.data
        )

    def test_validation(self):
        """ Assert data validation throws no error on valid JSON. """
        self.assertEqual(self.instance._data.get('string'), json.dumps('foo'))
        self.instance.clean()

    def test_validation_failure(self):
        """ Assert data validation raises exception on invalid JSON. """
        with self.assertRaises(ValidationError):
            self.instance._data['string'] = "not valid JSON"
            self.instance.clean()

    def test_form_validation__full_data(self):
        """ Ensure model form validates with empty data """
        form = modelform_factory(TestModel)
        f = form(data=self.instance.__dict__)
        f.full_clean()
        self.assertEqual(f.errors, {})

    def test_form_validation__empty_data(self):
        """ Ensure model form validates with empty data """
        self.instance.data = None
        self.instance.save()

        form = modelform_factory(TestModel)
        f = form(data=self.instance.__dict__)
        f.full_clean()
        self.assertEqual(f.errors, {})

    def test_update_data(self):
        """ Ensure update works as expected """
        self.instance.data.update({'int': 2000})
        self.assertEqual(
            self.instance.data,
            dict(
                int=2000,
                string='foo',
                date=self.now.isoformat(),
                list=[1, 'two'],
                dict=dict(a=1)
            )
        )
