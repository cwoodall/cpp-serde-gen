#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '',
    'author': 'Christopher Woodall',
    'url': '',
    'download_url': '',
    'author_email': 'chris@cwoodall.com',
    'version': '0.2',
    'install_requires': ['nose', 'clang', 'ccsyspath', 'cogapp'],
    'packages': ['cpp_serde_gen', 'cpp_serde_gen.serdes'],
    'name': 'cpp_serde_gen',
    'test_suite': 'nose.collector'
}

setup(**config)
