from setuptools import setup
import os

from django_hstore_mixin import get_version


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name='django-hstore-mixin',
    version=get_version(),
    description="Retain data type with Django-hstore",
    long_description=open('README.md').read(),
    author='Anthony Lukach',
    maintainer='Osprey Informatics Ltd',
    maintainer_email='admin@ospreyinformatics.com',
    license=open('LICENSE').read(),
    url='https://github.com/ospreyinformatics/django-hstore_mixin',
    download_url='https://github.com/ospreyinformatics/django-hstore_mixin/releases',
    packages=get_packages('django_hstore_mixin'),
    package_data=get_package_data('django_hstore_mixin'),
    install_requires=['django>=1.5', 'django_hstore>=1.2.4'],
)
