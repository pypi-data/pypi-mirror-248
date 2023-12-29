# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lkmlfmt']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'lark>=1.1.5,<2.0.0', 'shandy-sqlfmt>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['lkmlfmt = lkmlfmt.command:run']}

setup_kwargs = {
    'name': 'lkmlfmt',
    'version': '0.0.14',
    'description': '',
    'long_description': '# lkmlfmt\nlkmlfmt formats your LookML files including embedded SQL and HTML.\n\n## Installation\n```sh\npip install lkmlfmt\n```\n\n## CLI\nUse `lkmlfmt` command to format your LookML file(s).\nFor further information, use `--help` option.\n\n```sh\nlkmlfmt [OPTIONS] [FILE]...\n```\n\n## API\n```python\nfrom lkmlfmt import fmt\n\nlkml = fmt("""\\\nview: view_name {\n  derived_table: {\n    sql:\n    with cte as (\n      select col1, col2 from tablename\n      where ts between current_date()-7 and current_date())\n    select {% if true %} col1 {% else %} col2 {% endif %} from cte\n    ;;\n  }\n}\n""")\n\nassert lkml == """\\\nview: view_name {\n  derived_table: {\n    sql:\n      with\n        cte as (\n          select col1, col2\n          from tablename\n          where ts between current_date() - 7 and current_date()\n        )\n      select\n        {% if true %} col1\n        {% else %} col2\n        {% endif %}\n      from cte\n    ;;\n  }\n}\n"""\n```\n\n## GitHub Actions\nTo check if your LookML files are formatted.\n\n```yaml\non: [pull_request]\njobs:\n  format-check:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - uses: actions/setup-python@v4\n        with:\n          # \'>=3.11\' is required\n          python-version: \'3.11\'\n\n      # you should specify the version of lkmlfmt!\n      - run: pip install lkmlfmt\n      - run: lkmlfmt --check path/to/lookml/file/or/directory\n```\n\nTo format arbitrary branch and create pull request.\n\n```yaml\non: [workflow_dispatch]\njobs:\n  format-pr:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - uses: actions/setup-python@v4\n        with:\n          # \'>=3.11\' is required\n          python-version: \'3.11\'\n\n      # you should specify the version of lkmlfmt!\n      - run: pip install lkmlfmt\n      - run: lkmlfmt path/to/lookml/file/or/directory\n\n      # check the documentation especially about workflow permissions\n      # https://github.com/marketplace/actions/create-pull-request\n      - uses: peter-evans/create-pull-request@v5\n        with:\n          branch: format/${{ github.ref_name }}\n```\n\n## Feedback\nI\'m not ready to accept pull requests, but your feedback is always welcome.\nIf you find any bugs, please feel free to create an issue.\n\n## See also\nIn default, lkmlfmt formats embedded sql using sqlfmt.\n\n* [sqlfmt](https://github.com/tconbeer/sqlfmt)\n\nYou can install plugins to change the format of embeded looker expression, sql or html.\nThey are distributed under their own licenses, so please check if they are suitable for your purpose.\n\n* [lkmlfmt-djhtml](https://github.com/kitta65/lkmlfmt-djhtml)\n',
    'author': 'dr666m1',
    'author_email': 'skndr666m1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
