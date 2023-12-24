# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nick_derobertis_site',
 'nick_derobertis_site.api',
 'nick_derobertis_site.api.routers',
 'nick_derobertis_site.gen_content']

package_data = \
{'': ['*']}

install_requires = \
['awesome-panel-extensions',
 'derobertis-cv',
 'fastapi',
 'fire',
 'jupyterlab',
 'panel',
 'pydantic',
 'pydantic-to-typescript',
 'sentry-sdk',
 'uvicorn[standard]']

setup_kwargs = {
    'name': 'nick-derobertis-site',
    'version': '1.3.0',
    'description': "Nick DeRobertis' Personal Website",
    'long_description': "[![](https://codecov.io/gh/nickderobertis/nick-derobertis-site/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/nick-derobertis-site)\n[![PyPI](https://img.shields.io/pypi/v/nick-derobertis-site)](https://pypi.org/project/nick-derobertis-site/)\n![PyPI - License](https://img.shields.io/pypi/l/nick-derobertis-site)\n[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/nick-derobertis-site/)\n![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.10-blue)\n[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/nick-derobertis-site/)\n\n# Nick DeRobertis' Personal Website\n\n# nick-derobertis-site\n\n## Overview\n\nNick DeRobertis' Personal Website, built with Python, Panel, Bootstrap, and jQuery.\n\n## Links\n\nSee the website\n[at nickderobertis.com.](https://nickderobertis.com)\n\n# Developing\n\n## Backend Development\n\nRun `just dev-be` to run the backend server.\n\n## Frontend Development\n\nRun `just dev-fe` to run the frontend server. You may need to\ncd into the frontend/nick-derobertis-site directory and run `pnpm i` first.\n\n## QA\n\nMake sure you have Docker installed.\n\nRun `just qa` to start a production-like\nbuild. Run `./stop-docker.sh` to stop.\n\n## Development Status\n\nThis project is currently in early-stage development. There may be\nbreaking changes often. While the major version is 0, minor version\nupgrades will often have breaking changes.\n\n## Developing\n\nSee the [development guide](https://github.com/nickderobertis/nick-derobertis-site/blob/master/DEVELOPING.md) for development details.\n\n## Author\n\nCreated by Nick DeRobertis. MIT License.\n",
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
