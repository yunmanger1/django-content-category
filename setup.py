#!/usr/bin/env python
import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = 'django-content-category',
    version = '1.0.0',
    description = 'This django application gives category functionality. Can be used by other applications.',
    author = 'German Ilyin',
    author_email = 'germanilyin@gmail.com',
    url = 'https://github.com/yunmanger1/django-content-category/',
    license = 'WTFPL',
    long_description = read('README'),
    packages = ['category', 'category.templatetags', 'category.tests', 'category.utils'],
    package_data = {
        'category/fixtures': ['category/fixtures/*'],
        'category/static': ['category/static/*'],
        'category/templates': ['category/templates/*'],
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Plugins",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: Freeware",
        "Programming Language :: Python :: 2.6",
    ],
)
