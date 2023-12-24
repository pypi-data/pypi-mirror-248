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
    'version': '2.4.182',
    'description': 'Python async API for MISP.',
    'long_description': '**IMPORTANT NOTE**: This library will require **at least** Python 3.10 starting the 1st of January 2024. If you have legacy versions of python, please use the latest PyMISP version that will be released in December 2023, and consider updating your system(s). Anything released within the last 2 years will do, starting with Ubuntu 22.04.\n\n# PyMISP - Python Library to access MISP\n\n[![Documentation Status](https://readthedocs.org/projects/pymisp/badge/?version=latest)](http://pymisp.readthedocs.io/?badge=latest)\n[![Coverage Status](https://coveralls.io/repos/github/MISP/PyMISP/badge.svg?branch=main)](https://coveralls.io/github/MISP/PyMISP?branch=main)\n[![Python 3.8](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)\n[![PyPi version](https://img.shields.io/pypi/v/pymisp.svg)](https://pypi.python.org/pypi/pymisp/)\n[![Number of PyPI downloads](https://img.shields.io/pypi/dm/pymisp.svg)](https://pypi.python.org/pypi/pymisp/)\n\nPyMISP is a Python library to access [MISP](https://github.com/MISP/MISP) platforms via their REST API.\n\nPyMISP allows you to fetch events, add or update events/attributes, add or update samples or search for attributes.\n\n## Install from pip\n\n**It is strongly recommended to use a virtual environment**\n\nIf you want to know more about virtual environments, [python has you covered](https://docs.python.org/3/tutorial/venv.html)\n\nOnly basic dependencies:\n```\npip3 install pymisp\n```\n\nAnd there are a few optional dependencies:\n* fileobjects: to create PE/ELF/Mach-o objects\n* openioc: to import files in OpenIOC format (not really maintained)\n* virustotal: to query VirusTotal and generate the appropriate objects\n* docs: to generate te documentation\n* pdfexport: to generate PDF reports out of MISP events\n* url: to generate URL objects out of URLs with Pyfaup\n* email: to generate MISP Email objects\n* brotli: to use the brotli compression when interacting with a MISP instance\n\nExample:\n\n```\npip3 install pymisp[virustotal,email]\n```\n\n## Install the latest version from repo from development purposes\n\n**Note**: poetry is required; e.g., "pip3 install poetry"\n\n```\ngit clone https://github.com/MISP/PyMISP.git && cd PyMISP\ngit submodule update --init\npoetry install -E fileobjects -E openioc -E virustotal -E docs -E pdfexport -E email\n```\n\n### Running the tests\n\n```bash\npoetry run pytest --cov=pymisp tests/test_*.py\n```\n\nIf you have a MISP instance to test against, you can also run the live ones:\n\n**Note**: You need to update the key in `tests/testlive_comprehensive.py` to the automation key of your admin account.\n\n```bash\npoetry run pytest --cov=pymisp tests/testlive_comprehensive.py\n```\n\n## Samples and how to use PyMISP\n\nVarious examples and samples scripts are in the [examples/](examples/) directory.\n\nIn the examples directory, you will need to change the keys.py.sample to enter your MISP url and API key.\n\n```\ncd examples\ncp keys.py.sample keys.py\nvim keys.py\n```\n\nThe API key of MISP is available in the Automation section of the MISP web interface.\n\nTo test if your URL and API keys are correct, you can test with examples/last.py to\nfetch the events published in the last x amount of time (supported time indicators: days (d), hours (h) and minutes (m)).\nlast.py\n```\ncd examples\npython3 last.py -l 10h # 10 hours\npython3 last.py -l 5d  #  5 days\npython3 last.py -l 45m # 45 minutes\n```\n\n\n## Debugging\n\nYou have two options here:\n\n1. Pass `debug=True` to `PyMISP` and it will enable logging.DEBUG to stderr on the whole module\n\n2. Use the python logging module directly:\n\n```python\n\nimport logging\nlogger = logging.getLogger(\'pymisp\')\n\n# Configure it as you wish, for example, enable DEBUG mode:\nlogger.setLevel(logging.DEBUG)\n```\n\nOr if you want to write the debug output to a file instead of stderr:\n\n```python\nimport pymisp\nimport logging\n\nlogger = logging.getLogger(\'pymisp\')\nlogging.basicConfig(level=logging.DEBUG, filename="debug.log", filemode=\'w\', format=pymisp.FORMAT)\n```\n\n## Test cases\n\n1. The content of `mispevent.py` is tested on every commit\n2. The test cases that require a running MISP instance can be run the following way:\n\n\n```bash\n# From poetry\n\npytest --cov=pymisp tests/test_*.py tests/testlive_comprehensive.py:TestComprehensive.[test_name]\n\n```\n\n## Documentation\n\nThe documentation is available [here](https://pymisp.readthedocs.io/en/latest/).\n\n### Jupyter notebook\n\nA series of [Jupyter notebooks for PyMISP tutorial](https://github.com/MISP/PyMISP/tree/main/docs/tutorial) are available in the repository.\n\n## Everything is a Mutable Mapping\n\n... or at least everything that can be imported/exported from/to a json blob\n\n`AbstractMISP` is the master class, and inherits from `collections.MutableMapping` which means\nthe class can be represented as a python dictionary.\n\nThe abstraction assumes every property that should not be seen in the dictionary is prepended with a `_`,\nor its name is added to the private list `__not_jsonable` (accessible through `update_not_jsonable` and `set_not_jsonable`.\n\nThis master class has helpers that make it easy to load, and export to, and from, a json string.\n\n`MISPEvent`, `MISPAttribute`, `MISPObjectReference`, `MISPObjectAttribute`, and `MISPObject`\nare subclasses of AbstractMISP, which mean that they can be handled as python dictionaries.\n\n## MISP Objects\n\nCreating a new MISP object generator should be done using a pre-defined template and inherit `AbstractMISPObjectGenerator`.\n\nYour new MISPObject generator must generate attributes and add them as class properties using `add_attribute`.\n\nWhen the object is sent to MISP, all the class properties will be exported to the JSON export.\n\n## Installing PyMISP on a machine with no internet access\n\nThis is done using poetry and you need to have this repository cloned on your machine.\nThe commands below have to be run from inside the cloned directory.\n\n\n1. From a machine with access to the internet, get the dependencies:\n\n```bash\nmkdir offline\npoetry export --all-extras  > offline/requirements.txt\npoetry run pip download -r offline/requirements.txt -d offline/packages/\n```\n\n2. Prepare the PyMISP Package\n\n```bash\npoetry build\nmv dist/*.whl offline/packages/\n```\n\n2. Copy the content of `offline/packages/` to the machine with no internet access.\n\n3. Install the packages:\n\n```bash\npython -m pip install --no-index --no-deps packages/*.whl\n```\n\n# License\n\nPyMISP is distributed under an [open source license](./LICENSE). A simplified 2-BSD license.\n\n',
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
