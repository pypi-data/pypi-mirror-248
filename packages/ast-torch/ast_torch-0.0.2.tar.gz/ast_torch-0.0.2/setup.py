# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ast_torch']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'ast-torch',
    'version': '0.0.2',
    'description': 'ast - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# AST\nImplementation of AST from the paper: "AST: Audio Spectrogram Transformer\' in PyTorch and Zeta.\n\n## Install\n`pip3 install ast-torch`\n\n## Usage\n```\n\n```\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/AST',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
