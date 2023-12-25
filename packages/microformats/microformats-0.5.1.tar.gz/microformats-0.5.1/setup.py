# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mf']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'easyuri>=0.1.2',
 'mf2py>=2.0.1,<3.0.0',
 'txtint>=0.1.2']

entry_points = \
{'console_scripts': ['mf = mf:main']}

setup_kwargs = {
    'name': 'microformats',
    'version': '0.5.1',
    'description': 'tools for microformats production, consumption and analysis',
    'long_description': '[microformats][0] are the simplest way to openly publish contacts, events,\nreviews, recipes, and other structured information on the web.\n\n    >>> import mf\n    >>> url = "https://alice.example"\n    >>> doc = f\'\'\'\n    ... <p class=h-card><a href={url}>Alice</a></p>\n    ... <ul class=h-feed>\n    ... <li class=h-entry>foo\n    ... <li class=h-entry>bar\n    ... </ul>\n    ... \'\'\'\n    >>> page = mf.parse(doc=doc, url=url)\n\n    # TODO >>> dict(page)\n    # TODO >>> page.json\n\n    >>> card = page["items"][0]\n    >>> card["type"]\n    [\'h-card\']\n    >>> card["properties"]\n    {\'name\': [\'Alice\'], \'url\': [\'https://alice.example\']}\n    >>> feed = page["items"][1]\n    >>> feed["children"][0]["properties"]["name"]\n    [\'foo\']\n\n    >>> mf.util.representative_card(page, url)\n    {\'name\': [\'Alice\'], \'url\': [\'https://alice.example\']}\n    >>> mf.util.representative_feed(page, url)["items"][0]["name"]\n    [\'foo\']\n\n    # TODO >>> page.representative_card\n    # TODO {\'name\': [\'Alice\'], \'url\': [\'https://alice.example\']}\n    # TODO >>> page.representative_feed["items"][0]["name"]\n    # TODO [\'foo\']\n\nBased upon [`mf2util`][1].\n\n[0]: https://microformats.org/wiki/microformats\n[1]: https://github.com/kylewm/mf2util\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/python-microformats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
