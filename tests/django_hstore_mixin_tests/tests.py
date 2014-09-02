# -*- coding: utf-8 -*-
import datetime
import json

from django.core.exceptions import ValidationError
from django.test import TestCase

from django_hstore_mixin_tests.models import TestModel


class TestHstoreMixin(TestCase):

    def setUp(self):
        self.now = datetime.datetime.now()
        self.e = TestModel.objects.create(
            data=dict(
                int=1,
                string='foo',
                date=self.now,
                list=[1, 'two'],
                dict=dict(a=1)
            )
        )

    def test_setting(self):
        self.assertEqual(
            self.e._data,
            {
                'date': json.dumps(self.now.isoformat()),
                'int': '1',
                'list': '[1, "two"]',
                'string': '"foo"',
                'dict': '{"a": 1}'
            }
        )

        self.e.data['int'] = 3
        self.e.save()
        self.assertEqual(self.e._data['int'], '3')

        self.e.data['list'] = [2, 'three']
        self.e.save()
        self.assertEqual(self.e._data['list'], '[2, "three"]')

        self.e.data['string'] = 'Foo'
        self.e.save()
        self.assertEqual(self.e._data['string'], '"Foo"')

        self.e.data['dict'] = dict(a=2)
        self.e.save()
        self.assertEqual(self.e._data['dict'], '{"a": 2}')

    def test_getting(self):
        self.assertEqual(
            self.e.data,
            dict(int=1, string='foo', date=self.now.isoformat(), list=[1, 'two'], dict={'a': 1})
        )

        self.assertEqual(self.e.data.get('int'), 1)
        self.assertEqual(self.e.data.get('string'), 'foo')
        self.assertEqual(self.e.data.get('date'), self.now.isoformat())
        self.assertEqual(self.e.data.get('list'), [1, 'two'])
        self.assertEqual(self.e.data.get('dict'), {'a': 1})
        self.assertEqual(self.e.data.get('notThere'), None)
        self.assertEqual(self.e.data.get('notThere', 'Nope'), 'Nope')

        self.assertEqual(self.e.data['int'], 1)
        self.assertEqual(self.e.data['string'], 'foo')
        self.assertEqual(self.e.data['date'], self.now.isoformat())
        self.assertEqual(self.e.data['list'], [1, 'two'])
        self.assertEqual(self.e.data['dict'], {'a': 1})
        with self.assertRaises(KeyError):
            self.e.data['notThere']

    def test_comparison(self):
        self.assertTrue(
            self.e.data == dict(
                int=1,
                string='foo',
                date=self.now.isoformat(),
                list=[1, 'two'],
                dict={'a': 1}
            )
        )

    def test_validation(self):
        self.assertEqual(self.e._data.get('string'), json.dumps('foo'))
        self.e.clean()

        with self.assertRaises(ValidationError):
            self.e._data['string'] = "not valid JSON"
            self.e.clean()
