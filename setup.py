# -*- coding: utf-8 -*-
from __future__ import with_statement
from distutils.core import setup
from setuptools import find_packages

with open('README.rst') as readme:
    long_description = readme.read()

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n') if (line and not
                                                     line.startswith('--'))
    ]

setup(
    name='irclogs',
    version=__import__('irclogs').__version__,
    author='Bruno Renie',
    author_email='bruno@renie.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://logs.bruno.im',
    license='BSD',
    description='A web interface for IRC logs',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    install_requires=install_requires,
)
