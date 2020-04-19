#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Web Land Trajectory Service."""

import os
from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('CHANGES.rst').read()

tests_require = [
    'coverage>=4.5',
    'coveralls>=1.8',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'isort>4.3',
    'check-manifest>=0.40'
]

docs_require = [
    'Sphinx>=2.2',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
}

extras_require['all'] = [req for exts, reqs in extras_require.items() for req in reqs]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'Flask>=1.1.1',
    'Flask-Cors>=3.0.8',
    'Flask-Script>=2.0.6',
    'Flask-SQLAlchemy>=2.4.1',
    'GDAL>=2.4',
    'psycopg2>=2.8.3',
    'requests>=2.9.1',
    'SQLAlchemy==1.3.4',
    'shapely>=1.6',
    'Werkzeug>=0.16.1,<1', # Temp workaround https://github.com/noirbizarre/flask-restplus/issues/777
    'bdc-core @ git+git://github.com/brazil-data-cube/bdc-core.git@b-0.2#egg=bdc-core',
]

packages = find_packages()

g = {}
with open(os.path.join('wlts', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='wlts',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='Land Use Cover',
    license='MIT',
    author='INPE',
    author_email='brazildatacube@dpi.inpe.br',
    url='https://github.com/brazil-data-cube/wlts',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'wlts = wlts.cli:cli'
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)