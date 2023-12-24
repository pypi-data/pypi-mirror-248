# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_system',
 'webint_system.templates',
 'webint_system.templates.addresses']

package_data = \
{'': ['*']}

install_requires = \
['webagt>=0.0', 'webint>=0.0']

entry_points = \
{'webapps': ['system = webint_system:app']}

setup_kwargs = {
    'name': 'webint-system',
    'version': '0.0.29',
    'description': "manage your website's system",
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/webint-system',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
