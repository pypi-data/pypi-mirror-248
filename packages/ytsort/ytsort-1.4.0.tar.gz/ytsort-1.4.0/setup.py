# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ytsort']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress==1.6.2',
 'click>=8.0.3,<9.0.0',
 'colorama>=0.3.7,<0.4.0',
 'google-api-python-client>=2.8.0,<3.0.0']

entry_points = \
{'console_scripts': ['ytsort = ytsort.__main__:cli']}

setup_kwargs = {
    'name': 'ytsort',
    'version': '1.4.0',
    'description': 'Arrange downloaded youtube videos',
    'long_description': "# YTSort\n\nThis program sorts the already downloaded youtube videos present in a folder by renaming them and adding serial number before their names.\n\n# Requirements\n\nYoutube Data API v3 is required. Get it from [here](https://console.cloud.google.com/apis/library/youtube.googleapis.com?supportedpurview=project)\n\n# Install\n###### Recommended (To install pipx click [here](https://github.com/pypa/pipx#install-pipx))\n```\npipx install ytsort\n```\n\n###### or\n```\npip install ytsort\n```\n\n#### Or upgrade by:\n```\npipx upgrade ytsort\n```\n###### or\n```\npip install --upgrade ytsort\n```\n# Usage\n\nSet Youtube API Key to the environment variable 'YOUTUBE_DATA_API_KEY' (for ease of use, but not required).\n\n### Execute:\n```\nytsort\n```\n\n```\nUsage: ytsort [OPTIONS]\n\nOptions:\n\n  -c, --character TEXT    Character after serial.\n  -z, --zero              Add zero before serial numbers to make them all of\n                          equal length.\n  -x, --nozero            Don't add zero before serial numbers.\n  -d, --defaults          Change the default configurations and exit.\n  -r, --remove-serial     Remove the serial numbers from the local files upto\n                          the given character\n  --help                  Show this message and exit.\n```\n\n\n\n# Install from source\nPoetry is required. For installation click [here](https://python-poetry.org/docs/#installation).\n\n1. Download the source and install the dependencies by running:\n  \n   ``` \n   git clone https://github.com/aqdasak/YTSort.git\n   cd YTSort\n   poetry install\n   ```\n\n2. Not required but for ease of use\n \n   a) Set Youtube API Key to the environment variable 'YOUTUBE_DATA_API_KEY'\n\n   or\n \n   b) edit the `config.py`:\n\n      `'api_key': os.environ.get('YOUTUBE_DATA_API_KEY'),` to `'api_key': <Your Youtube API key>,`\n\n### Run\nIn the source folder containing pyproject.toml\n```\npoetry shell\n```\n\nthen cd into the folder containing youtube videos and execute:\n```\nytsort\n```\n",
    'author': 'Aqdas Ahmad Khan',
    'author_email': 'aqdasak@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aqdasak/YTSort/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
