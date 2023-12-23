# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_fullstack',
 'django_fullstack.core',
 'django_fullstack.core.handlers',
 'django_fullstack.core.management',
 'django_fullstack.core.management.commands',
 'django_fullstack.django_vite',
 'django_fullstack.django_vite.core',
 'django_fullstack.django_vite.templatetags',
 'django_fullstack.inertia',
 'django_fullstack.scripts',
 'django_fullstack.templatetags']

package_data = \
{'': ['*'],
 'django_fullstack': ['templates/react/*',
                      'templates/react/src/*',
                      'templates/react/src/Layout/*',
                      'templates/react/src/assets/*',
                      'templates/react/src/pages/*',
                      'templates/react_typescript/*',
                      'templates/react_typescript/public/*',
                      'templates/react_typescript/src/*',
                      'templates/react_typescript/src/Layout/*',
                      'templates/react_typescript/src/assets/*',
                      'templates/react_typescript/src/pages/*',
                      'templates/vue3/*',
                      'templates/vue3/src/*',
                      'templates/vue3/src/assets/*',
                      'templates/vue3/src/components/*',
                      'templates/vue3/src/pages/*',
                      'templates/vue3/src/public/*',
                      'templates/vue3_typescript/*',
                      'templates/vue3_typescript/src/*',
                      'templates/vue3_typescript/src/assets/*',
                      'templates/vue3_typescript/src/components/*',
                      'templates/vue3_typescript/src/pages/*',
                      'templates/vue3_typescript/src/public/*'],
 'django_fullstack.inertia': ['templates/*']}

install_requires = \
['Django>=4.0,<5.0', 'django-minify-html>=1.7.1,<2.0.0']

entry_points = \
{'console_scripts': ['django-fullstack = '
                     'django_fullstack.scripts.django_fullstack:run']}

setup_kwargs = {
    'name': 'django-fullstack',
    'version': '0.2.1',
    'description': "make your project frontendn + django with django-fullstack, it's so easy",
    'long_description': None,
    'author': 'Raja Sunrise',
    'author_email': 'rajasunsrise@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rajasunrise/django-fullstack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
