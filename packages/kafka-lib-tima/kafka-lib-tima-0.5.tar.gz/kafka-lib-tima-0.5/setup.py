from setuptools import setup, find_packages

setup(
    name='kafka-lib-tima',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'confluent_kafka',
    ],
)
