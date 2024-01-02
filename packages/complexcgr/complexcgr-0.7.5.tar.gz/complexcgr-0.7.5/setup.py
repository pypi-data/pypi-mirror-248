# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['complexcgr']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=10.0,<11.0',
 'biopython>=1.79,<2.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'tqdm>=4.61.2,<5.0.0']

setup_kwargs = {
    'name': 'complexcgr',
    'version': '0.7.5',
    'description': 'complex Chaos Game Representation for DNA',
    'long_description': None,
    'author': 'Jorge Avila',
    'author_email': 'jorgeavilacartes@gmail.com',
    'maintainer': 'Jorge Avila',
    'maintainer_email': 'jorgeavilacartes@gmail.com',
    'url': 'https://github.com/AlgoLab/complexCGR',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
