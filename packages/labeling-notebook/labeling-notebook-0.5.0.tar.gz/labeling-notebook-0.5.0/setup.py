# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labeling', 'labeling.notebook', 'labeling.plugin']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['label = labeling.__main__:main']}

setup_kwargs = {
    'name': 'labeling-notebook',
    'version': '0.5.0',
    'description': 'An image annotation or labeling tool for small project',
    'long_description': None,
    'author': 'Wanasit T',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
