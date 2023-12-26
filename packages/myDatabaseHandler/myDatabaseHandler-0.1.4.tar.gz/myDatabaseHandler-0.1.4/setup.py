# python3 setup.py sdist
# twine upload dist/*
# pip install myDatabaseHandler

from setuptools import setup, find_packages

setup(
    name='myDatabaseHandler',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'pymysql',
    ],
)
