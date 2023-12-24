# setup.py
from setuptools import setup, find_packages

setup(
    name='kafka-lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'confluent_kafka',
    ],
)
