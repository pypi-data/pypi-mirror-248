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
    'version': '0.0.1',
    'description': 'qformer - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n# Qformer\nImplementation of Qformer from BLIP2 in Zeta Lego blocks.\n\n## Install\n`pip3 install qformer`\n\n\n## Usage\n```python\nimport torch\nfrom qformer import ImgBlock\n\n\n# 3d tensor, B x SEQLEN x DIM\nx = torch.randn(1, 32, 1024)\nimage = torch.randn(1, 32, 1024)\n\nattn = ImgBlock(1024, 8, 1024)\nout = attn(x, image)\nprint(out.shape)\n```\n\n\n# License\nMIT\n\n\n\n',
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
