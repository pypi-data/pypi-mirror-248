import setuptools
from pathlib import Path

setuptools.setup(
    name='mdlogger',
    version=0.1,
    long_description=Path('README.rst').read_text(),
    packages=setuptools.find_packages(exclude=['logs', 'test'])
)
