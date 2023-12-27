# setup.py

from setuptools import setup, find_packages

setup(
    name='django_fonder',
    version='1.0.0',
    packages=find_packages(),
    package_data={
        'django_fonder': ['management/commands/*'],
    },
    install_requires=[
        'Django>=3.0',
    ],
)
