import setuptools
import sys

import pip

pip_version = tuple([int(x) for x in pip.__version__.split('.')[:3]])
if pip_version < (9, 0, 1) :
    raise RuntimeError('Version of pip less than 9.0.1, breaking python ' \
                       'version requirement support')

with open('version.txt', 'rb') as h:
    version = h.read().decode('utf-8').rstrip('\n')


setuptools.setup(
    name = 'loblaw-scheduler',
    version = version,
    include_package_data=True,
    zip_safe=False,
    py_modules = ['loblaw'],
    python_requires = '>=3.6',

    install_requires = [
        'icalendar',
        'requests',
        'Flask'
    ],

    author = 'Quinn Parrott',
    author_email = 'github@parrottq.ca',
    description = 'iCalendar adapter for Loblaw employee schedules',
    license = 'MIT',
    keywords = 'loblaw calendar'.split(' '),
    url = 'https://github.com/parrottq/loblaw-scheduler'
)
