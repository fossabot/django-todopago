#!/usr/bin/env python3

from setuptools import setup

setup(
    name='django_todopago',
    description='Library to integrate TodoPago into Django apps',
    author='Hugo Osvaldo Barrera',
    author_email='hugo@barrera.io',
    url='https://github.com/WhyNotHugo/django-todopago',
    license='ISC',
    packages=['django_todopago'],
    include_package_data=True,
    install_requires=[
        'django>=2.0',
        'suds-jurko',
        'requests',
    ],
    long_description=open('README.rst').read(),
    use_scm_version={
        'version_scheme': 'post-release',
        'write_to': 'django_todopago/version.py',
    },
    setup_requires=['setuptools_scm'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)
