from setuptools import setup

__version__ = '0.0.1'
__author__ = 'Gabriel Gene'

requirements = [
    'selenium==3.13.0',
    'psycopg2_binary==2.7.5',
    'psycopg2==2.7.5',
]

description = 'Bet crawlers'

setup(
    name='bet_crawlers',
    version=__version__,
    author=__author__,
    author_email='gabrielgene@gmail.com',
    url='https://github.com/gabrielgene/bet_crawlers',
    py_modules='betcrawlers',
    description=description,
    install_requires=requirements,
    include_package_data=True,
)
