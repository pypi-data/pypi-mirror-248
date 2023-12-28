# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyber-sentinels-helper-app',
 'cyber-sentinels-helper-app.contacts',
 'cyber-sentinels-helper-app.contacts.classes',
 'cyber-sentinels-helper-app.decorators',
 'cyber-sentinels-helper-app.file_manager',
 'cyber-sentinels-helper-app.notes',
 'cyber-sentinels-helper-app.outputs',
 'cyber-sentinels-helper-app.setup',
 'cyber-sentinels-helper-app.todo',
 'cyber-sentinels-helper-app.utils']

package_data = \
{'': ['*'],
 'cyber-sentinels-helper-app': ['.idea/*',
                                '.idea/inspectionProfiles/*',
                                'doc/*']}

install_requires = \
['prompt-toolkit>=3.0.43,<4.0.0', 'rich>=13.7.0,<14.0.0']

setup_kwargs = {
    'name': 'cyber-sentinels-helper-app',
    'version': '0.1.0',
    'description': 'coursework command project',
    'long_description': '# Cyber-Sentinels-helper-app\n\n## Project Description\n\nThe "Cyber-Sentinels-helper-app" project is a console application that allows users to maintain a phone book, a notebook, and a todo list.\n\n- **Phone Book:**\n  - Records have the following fields:\n    - Name\n    - Birthday\n    - Phones\n    - Email\n    - Address\n    - Status\n    - Note\n  - Functionality: adding new records, editing, deleting.\n\n- **Notebook:**\n  - Each note has fields:\n    - Title\n    - Notes\n  - Functionality: adding new notes, editing, deleting.\n\n- **Todo List:**\n  - Records have the following fields:\n    - Task\n    - Begin (time)\n    - End (time)\n    - Status (done, in process, ...)\n    - Tags\n  - Functionality: adding new records, editing, deleting.\n\nEach book can be stored in files and loaded into memory when the program is opened. There is also the ability to output information in Excel, JSON, and consoles view formats.\n\nAdditionally, the project implements functionality for navigating through the folders of the file system and sorting folders by various criteria.\n\n## Installation\n\nInstallation is done using `setuptools`. Project dependencies are listed in the `requirements.txt` file. They can be installed using the command:\n\n```bash\npip install -r requirements.txt\n\n## Usage\n\nThe project is utilized in the terminal console and is designed for the storage and processing of contacts, notes, and tasks. It also serves as a file manager.\n\n## Contribution\n\n1. **Siracenco Serghei** - Team Lead\n2. **Mageria Olga** – Scrum Master\n3. **Natalia Chepurna** – Developer\n4. **Victoria Kalachova** – Developer\n5. **Bogdan Soares** - Developer\n\n## License\n\nThis project is distributed under the MIT license. For more details, refer to the [LICENSE](LICENSE) file.',
    'author': 'siracencoserghei',
    'author_email': 'siracencoserghei@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
