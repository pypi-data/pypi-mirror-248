# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latti']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'latti',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'aprxi',
    'author_email': 'mail@aprxi.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
