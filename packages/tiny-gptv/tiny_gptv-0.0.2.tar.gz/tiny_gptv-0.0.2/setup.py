# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_gptv']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'tiny-gptv',
    'version': '0.0.2',
    'description': 'Tiny GPTV - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# TinyGPTV\nSimple Implementation of TinyGPTV in super simple Zeta lego blocks. Here all the modules from figure 2 are implemented in Zeta and Pytorch\n\n## Usage\n```python\nimport torch\nfrom tiny_gptv import TinyGPTVBlock\n\nx = torch.rand(2, 8, 512)\nlora_mha = TinyGPTVBlock(512, 8)\nout = lora_mha(x)\nprint(out.shape)\n\n```\n\n\n# Citation\n\n```bibtex\n@misc{yuan2023tinygptv,\n    title={TinyGPT-V: Efficient Multimodal Large Language Model via Small Backbones}, \n    author={Zhengqing Yuan and Zhaoxu Li and Lichao Sun},\n    year={2023},\n    eprint={2312.16862},\n    archivePrefix={arXiv},\n    primaryClass={cs.CV}\n}\n\n```\n\n# License\nMIT',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/TinyGPTV',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
