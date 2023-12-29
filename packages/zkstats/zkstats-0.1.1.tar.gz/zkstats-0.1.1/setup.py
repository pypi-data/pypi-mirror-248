# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zkstats']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0',
 'ezkl==5.0.8',
 'matplotlib>=3.8.2,<4.0.0',
 'numpy>=1.26.2,<2.0.0',
 'onnx>=1.15.0,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'scipy>=1.11.4,<2.0.0',
 'statistics>=1.0.3,<2.0.0',
 'torch>=2.1.1,<3.0.0']

entry_points = \
{'console_scripts': ['zkstats-cli = zkstats.cli:main']}

setup_kwargs = {
    'name': 'zkstats',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jern Kunpittaya',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
