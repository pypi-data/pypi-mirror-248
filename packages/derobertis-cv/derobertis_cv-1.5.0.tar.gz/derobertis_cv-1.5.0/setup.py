# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['derobertis_cv',
 'derobertis_cv.models',
 'derobertis_cv.models.grades',
 'derobertis_cv.plbuild',
 'derobertis_cv.plbuild.sources',
 'derobertis_cv.plbuild.sources.document',
 'derobertis_cv.pldata',
 'derobertis_cv.pldata._dev',
 'derobertis_cv.pldata._dev.skill',
 'derobertis_cv.pldata.constants',
 'derobertis_cv.pldata.courses',
 'derobertis_cv.pldata.cover_letters',
 'derobertis_cv.pldata.software',
 'derobertis_cv.pldata.software.yaml_',
 'derobertis_cv.pltemplates',
 'derobertis_cv.pltemplates.skills',
 'derobertis_cv.pltemplates.software']

package_data = \
{'': ['*'], 'derobertis_cv.plbuild': ['assets/images/*']}

install_requires = \
['PyPDF2<3',
 'PythonVideoConverter',
 'inflect',
 'jupyter-client',
 'jupyterlab',
 'pl-builder<1',
 'project-report==1.0.0a11',
 'pydantic<2',
 'pygithub==1.55',
 'pyyaml',
 'rich',
 'types-pyyaml',
 'types-requests',
 'weakreflist']

setup_kwargs = {
    'name': 'derobertis-cv',
    'version': '1.5.0',
    'description': "Nick DeRobertis' CV Data and pyexlatex Build",
    'long_description': "\n\n[![](https://codecov.io/gh/nickderobertis/derobertis-cv/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/derobertis-cv)\n[![PyPI](https://img.shields.io/pypi/v/derobertis-cv)](https://pypi.org/project/derobertis-cv/)\n![PyPI - License](https://img.shields.io/pypi/l/derobertis-cv)\n[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/derobertis-cv/)\n![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.10-blue)\n![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.10-blue)\n![Tests Run on Windows Python Versions](https://img.shields.io/badge/Tests%20Windows%2FPython-3.10-blue)\n[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/derobertis-cv/)\n\n\n#  derobertis-cv\n\n## Overview\n\nNick DeRobertis' CV Data and pyexlatex Build\n\n## Getting Started\n\nInstall `derobertis-cv`:\n\n```\npip install derobertis-cv\n```\n\nA simple example:\n\n```python\nimport derobertis_cv\n\n# Do something with derobertis_cv\n```\n\nSee a\n[more in-depth tutorial here.](\nhttps://nickderobertis.github.io/derobertis-cv/tutorial.html\n)\n\n## Links\n\nSee the\n[documentation here.](\nhttps://nickderobertis.github.io/derobertis-cv/\n)\n\n## Development Status\n\nThis project is currently in early-stage development. There may be\nbreaking changes often. While the major version is 0, minor version\nupgrades will often have breaking changes.\n\n## Developing\n\nSee the [development guide](\nhttps://github.com/nickderobertis/derobertis-cv/blob/master/DEVELOPING.md\n) for development details.\n\n## Author\n\nCreated by Nick DeRobertis. MIT License.\n\n",
    'author': 'Nick DeRobertis',
    'author_email': 'whoopnip@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
