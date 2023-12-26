# setup.py
from setuptools import setup, find_packages

setup(
    name='AsyncioPySide6',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'PySide6',
    ],
    entry_points={},
    test_suite='tests',
)
