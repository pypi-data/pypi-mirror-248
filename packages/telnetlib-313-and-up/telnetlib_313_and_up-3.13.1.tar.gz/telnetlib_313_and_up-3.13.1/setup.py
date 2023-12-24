# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telnetlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'telnetlib-313-and-up',
    'version': '3.13.1',
    'description': 'copy of telnetlib for python 3.13+',
    'long_description': "This is a copy of telnetlib for python3.13+\nIt was deprecated and is being removed in python3.13 but many people would still like their old code to work.\n\nJust install it with pip/poetry/etc for python3.13+ and your old telnetlib code should keep working.\n\nCurrently it is an exact copy(except for removing the derpracation warning),  \nbut I will accept patches for compatibility for future python versions.  \nNo extra options or feature or formatting fixes are likely.\n\nThe pep suggested telnetlib3 which has a differnt api and isn't a drop in replacemnet or Exscript which has an old copy of telnetlib  \nhttps://github.com/knipknap/exscript/blob/master/Exscript/protocols/telnetlib.py  \nwhich you can import with `import Exscript.protocols.telnetlib as telnetlib`  \nbut also a bunch of other stuff.\nAlso it requires you to modify your imports, this package doesn't.",
    'author': 'Guido van Rossum',
    'author_email': 'guido@python.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.13',
}


setup(**setup_kwargs)
