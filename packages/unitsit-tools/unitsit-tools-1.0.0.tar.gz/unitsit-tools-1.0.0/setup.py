from setuptools import setup, find_packages

setup(
    name='unitsit-tools',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # 'common_dependency1',
        # 'common_dependency2',
    ],
    extras_require={
        'toml': ['toml'],
        'asyncpg': ['asyncpg'],
        'psycopg': ['psycopg-binary'],
    },
    author='NoirPi',
    author_email='noirpi@noircoding.de',
    description='`unitsit-tools` is a Python package containing various utility modules for common tasks. '
                'Each module provides functionality for specific operations, '
                'such as working with different config formats, databases, logging, and miscellaneous tasks.',
    license='MIT',
)
