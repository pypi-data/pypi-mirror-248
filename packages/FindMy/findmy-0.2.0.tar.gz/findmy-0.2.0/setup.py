# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['findmy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.9.1,<4.0.0',
 'beautifulsoup4>=4.12.2,<5.0.0',
 'cryptography>=41.0.7,<42.0.0',
 'srp>=1.0.20,<2.0.0']

setup_kwargs = {
    'name': 'findmy',
    'version': '0.2.0',
    'description': "Everything you need to query Apple's Find My network!",
    'long_description': '# FindMy.py\n\nThe all-in-one library that provides everything you need\nto query Apple\'s FindMy network!\n\nThe current "Find My-scene" is quite fragmented, with code\nbeing all over the place across multiple repositories,\nwritten by [several authors](#Credits). This project aims to\nunify this scene, providing common building blocks for any\napplication wishing to integrate with the Find My network.\n\n## Features\n\n- [x] Works without any Apple devices\n- [x] Apple Account log-in\n- [x] SMS 2FA support\n- [x] Fetch location reports\n- [x] Generate and import accessory keys\n- [x] Both async and sync API\n- [x] Modular with a high degree of manual control\n\n## Roadmap\n\n- [ ] Trusted device 2FA\n    - Work has been done, but needs testing (I don\'t own any Apple devices)\n- [ ] Local anisette generation (without server)\n    - Can be done using [pyprovision](https://github.com/Dadoum/pyprovision/),\n      however I want to wait until Python wheels are available.\n\n# Installation\n\nTODO\n\n# Credits\n\nWhile I designed the library, the vast majority of the actual functionality\nis made possible by the following wonderful people and organizations:\n\n- @seemo-lab for [OpenHaystack](https://github.com/seemoo-lab/openhaystack/)\n  and their [research](https://doi.org/10.2478/popets-2021-0045);\n- @JJTech0130 for [Pypush](https://github.com/JJTech0130/pypush), providing the breakthrough necessary\n  for getting this to work without a Mac;\n- @biemster for [FindMy](https://github.com/biemster/FindMy), which is the main basis of this project;\n- @Dadoum for [pyprovision](https://github.com/Dadoum/pyprovision/) and\n  [anisette-v3-server](https://github.com/Dadoum/anisette-v3-server);\n- @nythepegasus for [GrandSlam](https://github.com/nythepegasus/grandslam/) SMS 2FA;\n- And probably more, so let me know! :D\n',
    'author': 'Mike Almeloo',
    'author_email': 'git@mikealmel.ooo',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
