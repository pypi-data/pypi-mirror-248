# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['objection_engine', 'objection_engine.beans', 'objection_engine.composers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'fonttools>=4.33.3,<5.0.0',
 'google-cloud-translate>=2.0.1,<3.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'morfessor>=2.0.6,<3.0.0',
 'moviepy>=1.0.3,<2.0.0',
 'numpy>=1.19.3,<2.0.0',
 'opencv-python>=4.5.5,<5.0.0',
 'polyglot>=16.7.4,<17.0.0',
 'praw>=7.5.0,<8.0.0',
 'pycld2>=0.41,<0.42',
 'pydub>=0.25.1,<0.26.0',
 'pyicu>=2.10.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'spacy>=3.1.4,<4.0.0',
 'spaw>=0.2,<0.3',
 'textblob>=0.17.1,<0.18.0',
 'tinydb>=4.7.0,<5.0.0',
 'toml>=0.10.2,<0.11.0',
 'torch>=1.13.1,<2.0.0',
 'transformers>=4.25.1,<5.0.0']

setup_kwargs = {
    'name': 'objection-engine',
    'version': '3.5.1',
    'description': 'Library that turns comment chains into Ace Attorney scenes, used in several bots',
    'long_description': None,
    'author': 'Luis Mayo Valbuena',
    'author_email': 'luismayovalbuena@outlook.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
