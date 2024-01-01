# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labeling_notebook_comic_ocr']

package_data = \
{'': ['*']}

install_requires = \
['comic-ocr>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'labeling-notebook-comic-ocr',
    'version': '0.1.0',
    'description': 'The `labeling-notebook` plugin for applying `comic-ocr` models.',
    'long_description': None,
    'author': 'Wanasit T',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
