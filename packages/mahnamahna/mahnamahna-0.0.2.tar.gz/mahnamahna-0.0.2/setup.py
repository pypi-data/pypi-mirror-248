# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mahnamahna', 'mahnamahna.voice']

package_data = \
{'': ['*']}

install_requires = \
['gTTS>=2.2.3,<3.0.0',
 'nltk>=3.8.1,<4.0.0',
 'pyglet>=2.0.10,<3.0.0',
 'pyttsx3>=2.90,<3.0',
 'sounddevice>=0.4.4,<0.5.0',
 'vosk>=0.3.32,<0.4.0',
 'webagt>=0.2.3,<0.3.0']

entry_points = \
{'console_scripts': ['transcribe = mahnamahna.voice:transcribe']}

setup_kwargs = {
    'name': 'mahnamahna',
    'version': '0.0.2',
    'description': 'Media (text/audio/video) analysis and manipulation',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/mahnamahna',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
