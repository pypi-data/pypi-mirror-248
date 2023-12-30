# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qformer']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'qformer',
    'version': '0.0.3',
    'description': 'qformer - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n# Qformer\nImplementation of Qformer from BLIP2 in Zeta Lego blocks. The implementation is here straight from Figure 2. In particular the image block and text block.\n\n## Install\n`pip3 install qformer`\n\n\n## Usage\n```python\nimport torch\nfrom qformer import QFormer\n\nx = torch.randn(1, 32, 512)\nimg = torch.randn(1, 32, 512)\n\nqformer = QFormer(512, 8, 8, 0.1, 2, 2)\ny = qformer(x, img)\nprint(y.shape)\n```\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/qformer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
