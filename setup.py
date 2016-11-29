#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

install_requires = [
    'talisker[prometheus]',
    'Flask',
]

setup(
    name='hello-talisker-prometheus',
    version='0.0.1',
    description="Flask + Talisker + Prometheus multiprocess test app",
    long_description=readme,
    author="Maximiliano Bertacchini",
    author_email='maxiberta@gmail.com',
    url='https://github.com/maxiberta/multiprocess-gunicorn-prometheus-client',
    packages=find_packages(),
    license="MIT",
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: System :: Logging',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=install_requires,
)
