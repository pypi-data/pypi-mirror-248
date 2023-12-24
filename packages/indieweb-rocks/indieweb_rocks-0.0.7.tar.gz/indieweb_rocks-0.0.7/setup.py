# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indieweb_rocks', 'indieweb_rocks.templates']

package_data = \
{'': ['*'],
 'indieweb_rocks': ['static/*', 'static/cc/*'],
 'indieweb_rocks.templates': ['toolbox/*']}

install_requires = \
['micropub>=0.0',
 'phonenumbers>=8.12.55,<9.0.0',
 'python-whois>=0.8.0,<0.9.0',
 'svglib>=1.3.0,<2.0.0',
 'typesense>=0.18.0,<0.19.0',
 'webint-data>=0.0',
 'webint-guests>=0.0',
 'webint-owner>=0.0',
 'webint-system>=0.0',
 'webint>=0.0']

entry_points = \
{'websites': ['indieweb_rocks = indieweb_rocks.__web__:app']}

setup_kwargs = {
    'name': 'indieweb-rocks',
    'version': '0.0.7',
    'description': 'IndieWeb validator',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
