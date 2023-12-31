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
    'version': '0.0.5',
    'description': 'Tiny GPTV - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# TinyGPTV\nSimple Implementation of TinyGPTV in super simple Zeta lego blocks. Here all the modules from figure 2 are implemented in Zeta and Pytorch.\n\nThe flow is the following:\nx -> skip connection -> layer norm -> lora -> mha + lora -> residual_rms_norm -> original_skip_connection -> mlp + rms norm\n\n\n## Install\n`pip3 install tiny-gptv`\n\n\n## Usage\n\n### TinyGPTVBlock, Figure3 (c):\n- Layernorm\n- MHA\n- Lora\n- QK Norm\n- RMS Norm\n- MLP\n\n\n```python\nimport torch\nfrom tiny_gptv.blocks import TinyGPTVBlock\n\n# Random tensor, replace with your input data\nx = torch.rand(2, 8, 512)\n\n# TinyGPTVBlock\nblock = TinyGPTVBlock(512, 8, depth=10)\n\n# Print the block\nprint(block)\n\n# Forward pass\nout = block(x)\n\n# Print the output shape\nprint(out.shape)\n\n\n```\n\n### Figure3 (b) Lora Module for LLMS Block\n- MHA,\n- Lora,\n- Normalization,\n- MLP\n- Skip connection\n- Split then add\n\n```python\nimport torch\nfrom tiny_gptv import LoraMHA\n\nx = torch.rand(2, 8, 512)\nblock = LoraMHA(512, 8)\nout = block(x)\nprint(out.shape)\n\n```\n\n\n# Citation\n\n```bibtex\n@misc{yuan2023tinygptv,\n    title={TinyGPT-V: Efficient Multimodal Large Language Model via Small Backbones}, \n    author={Zhengqing Yuan and Zhaoxu Li and Lichao Sun},\n    year={2023},\n    eprint={2312.16862},\n    archivePrefix={arXiv},\n    primaryClass={cs.CV}\n}\n\n```\n\n# License\nMIT',
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
