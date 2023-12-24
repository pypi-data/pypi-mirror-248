# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['incolume', 'incolume.py.changelog']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.5,<9.0.0', 'toml[tomli]>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['changelog = incolume.py.changelog.cli:changelog',
                     'gchangelog = incolume.py.changelog.cli:changelog',
                     'gcl = incolume.py.changelog.cli:changelog',
                     'gencl = incolume.py.changelog.cli:changelog']}

setup_kwargs = {
    'name': 'incolume-py-changelog',
    'version': '0.3.0rc1',
    'description': 'Generate CHANGELOG.md',
    'long_description': '# Python Incolume Utils\n\n--------\n\n_Projeto desenvolvido e administrado incolume.com.br_\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/incolumepy.makefilelicense)\n[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)\n[![Tests CI/CD](https://github.com/development-incolume/incolume.py.changelog/actions/workflows/tests-gwa-ci-cd.yml/badge.svg)](https://github.com/development-incolume/incolume.py.changelog/actions/workflows/tests-gwa-ci-cd.yml)\n![PyPI - Status](https://img.shields.io/pypi/status/incolumepy.makefilelicense)\n[![GitHub Actions (Tests)](https://github.com/development-incolume/incolume.py.changelog/workflows/Tests/badge.svg)](https://github.com/development-incolume/incolume.py.changelog/)\n[![codecov](https://codecov.io/gh/incolumepy/incolumepy.makefilelicense/branch/main/graph/badge.svg?token=QFULL7R8HX)](https://codecov.io/gh/incolumepy/incolumepy.makefilelicense)\n![PyPI](https://img.shields.io/pypi/v/incolumepy.makefilelicense)\n![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/incolumepy/incolumepy.makefilelicense?logo=tag)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/incolumepy.makefilelicense)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/incolumepy.makefilelicense)\n![PyPI - License](https://img.shields.io/pypi/l/incolumepy.makefilelicense)\n!["Code style: blue"](https://img.shields.io/badge/code%20style-blue-black)\n!["Code style: ruff"](https://img.shields.io/badge/code%20style-ruff-black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=4444444)](https://pycqa.github.io/isort/)\n[![Docstring style: pydocstyle](https://img.shields.io/badge/%20Docstring%20Style-PyDocStyle-%231674b1?style=flat&labelColor=444444)](http://www.pydocstyle.org/en/stable/)\n[![Linter: mypy](https://img.shields.io/badge/%20Linter-Mypy-%231674b1?style=flat&labelColor=4444444)](https://mypy.readthedocs.io/en/stable/)\n[![Linter: pylint](https://img.shields.io/badge/%20Linter-pylint-%231674b1?style=flat&labelColor=4444444)](https://pylint.pycqa.org/en/latest/)\n[![Linter: flake8](https://img.shields.io/badge/%20Linter-flake8-%231674b1?style=flat&labelColor=4444444)](https://flake8.pycqa.org/en/latest/)\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/incolumepy/incolumepy.makefilelicense)\n![GitHub repo size](https://img.shields.io/github/repo-size/incolumepy/incolumepy.makefilelicense)\n![GitHub issues](https://img.shields.io/github/issues/incolumepy/incolumepy.makefilelicense)\n![GitHub closed issues](https://img.shields.io/github/issues-closed/incolumepy/incolumepy.makefilelicense)\n![GitHub closed issues by-label](https://img.shields.io/github/issues-closed/incolumepy/incolumepy.makefilelicense/enhancement)\n![GitHub issues by-label](https://img.shields.io/github/issues/incolumepy/incolume.py.changelog/bug)\n![GitHub issues by-label](https://img.shields.io/github/issues/incolumepy/incolume.py.changelog/enhancement)\n[![Downloads](https://pepy.tech/badge/incolume-py-changelog)](https://pepy.tech/project/incolume-py-changelog)\n[![Downloads](https://pepy.tech/badge/incolume-py-changelog/month)](https://pepy.tech/project/incolume-py-changelog)\n[![Downloads](https://pepy.tech/badge/incolume-py-changelog/week)](https://pepy.tech/project/incolume-py-changelog)\n---\n\nEste gera o Changelog a partir dos registros encontrados em `git tag -n`.\n\n## Instalar o pacote\n\n### Instalação com pip\n```shell\npip install incolume.py.changelog\n```\n### Instalação com pipenv\n```shell\npipenv install incolume.py.changelog\n```\n\n### Instalação com poetry\n```shell\npoetry add incolume.py.changelog\n```\n\n```shell\npoetry add git+https://gitlab.com/development-incolume/incolumepy.utils.git#main\n```\n\n## Atualizar o pacote\n### Atualização com pip\n```shell\npip install -U incolume.py.changelog\n```\n### Atualização com pipenv\n```shell\npipenv update incolume.py.changelog\n```\n### Atualização com poetry\n```shell\npoetry update incolume.py.changelog\n```\n\n```shell\npoetry update git+https://gitlab.com/development-incolume/incolumepy.utils.git#main\n```\n\n## Gerar pacote a partir dos fontes para instalação\n\n```shell\npoetry build\n```\n\n## Documentação detalhada\nExemplos da API disponíveis em [docs/api](\'docs/api/index.md\')\n\n',
    'author': 'britodfbr',
    'author_email': 'contato@incolume.com.br',
    'maintainer': 'britodfbr',
    'maintainer_email': 'contato@incolume.com.br',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
