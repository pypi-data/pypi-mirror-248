# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymisp_async', 'pymisp_async.tools']

package_data = \
{'': ['*'], 'pymisp_async': ['data/*']}

install_requires = \
['aiohttp>=3.9.1,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'deprecated>=1.2.14,<2.0.0',
 'jsonschema>=4.20.0,<5.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.31.0,<3.0.0']

extras_require = \
{'brotli': ['urllib3[brotli]'],
 'docs': ['sphinx-autodoc-typehints>=1.25.2,<2.0.0',
          'recommonmark>=0.7.1,<0.8.0'],
 'docs:python_version < "3.9"': ['Sphinx<7.2', 'Sphinx<7.2'],
 'docs:python_version >= "3.9"': ['Sphinx>=7.2,<8.0', 'Sphinx>=7.2,<8.0'],
 'email': ['extract_msg>=0.47.0,<0.48.0',
           'RTFDE>=0.1.1,<0.2.0',
           'oletools>=0.60.1,<0.61.0'],
 'fileobjects': ['python-magic>=0.4.27,<0.5.0',
                 'pydeep2>=0.5.1,<0.6.0',
                 'lief>=0.13.2,<0.14.0'],
 'openioc': ['beautifulsoup4>=4.12.2,<5.0.0'],
 'pdfexport': ['reportlab>=4.0.8,<5.0.0'],
 'url': ['pyfaup>=1.2,<2.0'],
 'virustotal': ['validators>=0.22.0,<0.23.0']}

setup_kwargs = {
    'name': 'pymisp-async',
    'version': '2.4.182a3',
    'description': 'Python async API for MISP.',
    'long_description': '# **Advisory**\n\n**This library is an experimental project porting the original PyMISP project to python async to address I/O bound processing difficulties often encountered when using large MISP instances.**\n\n**It is an ALPHA release, this code has not been tested, USE AT YOUR OWN RISK!**\n\n# PyMISP - Python Library to access MISP\n\nPyMISP is a Python library to access [MISP](https://github.com/MISP/MISP) platforms via their REST API.\n\nPyMISP allows you to fetch events, add or update events/attributes, add or update samples or search for attributes.\n\nThis project aims at porting the original PyMISP project to Python async using the `aiohttp` library instead of the synchronous `requests` library.\n\n## Install from pip\n\n**It is strongly recommended to use a virtual environment**\n\nIf you want to know more about virtual environments, [python has you covered](https://docs.python.org/3/tutorial/venv.html)\n\nOnly basic dependencies:\n```\npip3 install pymisp-async\n```\n\n## Install the latest version from repo from development purposes\n\n**Note**: poetry is required; e.g., "pip3 install poetry"\n\n```\ngit clone https://github.com/pixmaip/PyMISP-async.git && cd PyMISP-async\ngit submodule update --init\npoetry install\n```\n\n## Usage\n\nInitialize the `PyMISP` object using the asynchronous context manager:\n```\nasync with PyMISP(url, key) as misp_obj:\n    events = await misp_obj.events()\n```\n\n## Documentation\n\nThe official MISP documentation is available [here](https://pymisp.readthedocs.io/en/latest/).\n\nAll `async` functions present in this library use the same API as the original MISP package.\n\n# License\n\nPyMISP is distributed under an [open source license](./LICENSE). A simplified 2-BSD license.\n\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MISP/PyMISP',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
