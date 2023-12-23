from setuptools import setup, find_packages

setup(
    name = 'cpbox',
    version = '1.5.36',
    keywords = ('cpbox'),
    description = 'cp tool box',
    license = '',
    install_requires = [
        'six',
        'ruamel.yaml==0.18.5',
        'Jinja2',
        'netaddr',
        'requests',
        'tzlocal==2.1',
        'redis',
        'configparser==3.7.4',
        ],

    scripts = [],

    author = 'http://www.liaohuqiu.net',
    author_email = 'liaohuqiu@gmail.com',
    url = '',

    packages = find_packages(),
    platforms = 'any',
)
