# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scythe_cli',
 'scythe_cli.application',
 'scythe_cli.ui',
 'scythe_cli.ui.widgets']

package_data = \
{'': ['*'], 'scythe_cli.ui': ['styles/*']}

install_requires = \
['arc-cli>=8.6.2,<9.0.0',
 'hishel>=0.0.20,<0.0.21',
 'httpx>=0.24.0,<0.25.0',
 'keyring>=23.13.1,<24.0.0',
 'msgspec>=0.15.1,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'textual>=0.45.1,<0.46.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['scythe = scythe_cli.application.application:scythe']}

setup_kwargs = {
    'name': 'scythe-cli',
    'version': '1.4.2',
    'description': 'A Harvest is always better with a good tool',
    'long_description': '# Scythe\n\n![Scythe TUI](./images/cover.svg)\n\nScythe is a TUI and set of CLI utilties for interacting with the Harvest Time tracking Application\n\n## Installation\n\nInstallable via pip/pipx (pipx is recommended)\n\n```\npipx install scythe-cli\n```\n\n## Setup\n\nFirst, you need to authenticate Scythe to your harvest account.\n\nTo do this, run the following command:\n\n```\nscythe init\n```\n\nThis will open a new browser tab to perform an OAuth flow with Harvest. Once you have authenticated, you will be redirected to a page with a code. Copy this code and paste it into the terminal.\n\n## Usage\n\n### TUI\nStart the TUI with\n\n```\nscythe\n```\n\nThe interface has the following features:\n\n- View all timers for a given day\n- Start a new timer\n- Stop a running timer\n- Edit a Timer\n- Delete a Timer\n\n\n### CLI\nThe CLI also has a few other utilties:\n\n`scythe timer` - The Scythe Timer namespace has some utilties for interacting with timers. `scythe timer --help` for more info\n\n`scythe projects` - List all the projects and tasks that you have access to\n\n\n#### Quickstarting\nQuickstarting is a feature of Scythe that allows you to start a timer with a single command. This is useful for setting up a timer for a task that you do frequently.\n\nTo create a new quickstart entry run:\n\n```\nscythe quickstart add <name>\n```\n\nThis will create a new quickstart entry with the name `<name>`. It will prompt you with a list of projects and tasks to choose from (And optionally, a note & a command to execute after the timer start). Once you have completed the prompt, you can start the timer with:\n\n```\nscythe quickstart <name>\n```\n\nThis will start a timer with the details you entered when creating the quickstart entry and will execute the command you entered (if any).\n\n`\n',
    'author': 'Sean Collings',
    'author_email': 'me@seancollings.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/seanrcollings/scythe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
