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
    'version': '0.0.5',
    'description': 'ast - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# AST\nImplementation of AST from the paper: "AST: Audio Spectrogram Transformer\' in PyTorch and Zeta. In this implementation we basically take an 2d input tensor representing audio -> then patchify it -> linear proj -> then position embeddings -> then attention and feedforward in a loop for layers. Please Join Agora and tag me if this could be improved in any capacity.\n\n## Install\n`pip3 install ast-torch`\n\n## Usage\n\n```python\nimport torch\nfrom ast_torch.model import ASTransformer\n\n# Create dummy data\nx = torch.randn(2, 16)\n\n# Initialize model\nmodel = ASTransformer(\n    dim=4, seqlen=16, dim_head=4, heads=4, depth=2, patch_size=4\n)\n\n# Run model and print output shape\nprint(model(x).shape)\n\n\n```\n\n\n# Citation\n```bibtex\n@misc{gong2021ast,\n    title={AST: Audio Spectrogram Transformer}, \n    author={Yuan Gong and Yu-An Chung and James Glass},\n    year={2021},\n    eprint={2104.01778},\n    archivePrefix={arXiv},\n    primaryClass={cs.SD}\n}\n\n```\n\n# License\nMIT',
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
