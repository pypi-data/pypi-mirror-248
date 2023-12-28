# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfpwm']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'dfpwm',
    'version': '0.1.4',
    'description': 'DFPWM convertor for Python',
    'long_description': '# DFPWM\n\nDFPWM convertor for Python\n\n## Usage\n\n```python\nfrom pathlib import Path\nimport soundfile as sf  # for reading audio\nimport dfpwm\n\ndata, sample_rate = sf.read(\'./someaudio.mp3\')  # read audio\n\n# If sample rate is not 48000, may get strange result\n# use `dfpwm.resample(...)` to resample\nif sample_rate != dfpwm.SAMPLE_RATE:\n    raise ValueError(f"{sample_rate} != {dfpwm.SAMPLE_RATE}")\n\nif len(data.shape) != 0 and data.shape[1] > 1:\n    data = data[:, 0]  # get channel 0\n\ndata = dfpwm.compressor(channel0)  # convert\nPath(\'out.dfpwm\').write_bytes(data)  # write result to file\n```\n\n## Build from source\n\n### Clone\n\n```shell\ngit clone https://github.com/CyanChanges/python-dfpwm.git python-dfpwm\ncd python-dfpwm\n```\n\n### Build\nThis project use `poetry` to build,\nMake sure `poetry` is installed.\n\n```shell\npoetry build -f sdist\n```\n\n',
    'author': 'cyan',
    'author_email': 'contact@cyans.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
