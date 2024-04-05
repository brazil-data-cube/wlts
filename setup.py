#
# This file is part of WLTS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Web Land Trajectory Service."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('CHANGES.rst').read()

tests_require = [
    'coverage>=4.5',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'isort>4.3',
    'check-manifest>=0.40'
]

docs_require = [
    'Sphinx>=2.2,<4',
    'sphinx_rtd_theme',
    'sphinx-copybutton',
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
    'Flask>=1.1.1,<2',
    'Flask-SQLAlchemy>=2.4.1',
    'requests>=2.9.1',
    'SQLAlchemy==1.3.4',
    'shapely>=1.6',
    'jsonschema>=3.2',
    'pyproj>=2',
    'OWSLib==0.28.1',
    'geojson==2.5.0',
    'MarkupSafe==2.0.1',
    'rasterio>=1.1.2,<2',
    'bdc-auth-client @ git+https://github.com/brazil-data-cube/bdc-auth-client@v0.2.3',
    'lccs-db @ git+https://github.com/brazil-data-cube/lccs-db@v0.8.1',
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
    license='GPLv3',
    author='INPE',
    author_email='brazildatacube@dpi.inpe.br',
    url='https://github.com/brazil-data-cube/wlts',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={},
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GPL v3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
