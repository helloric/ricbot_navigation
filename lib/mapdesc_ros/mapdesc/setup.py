#!/usr/bin/env python3
import os
from setuptools import setup, find_packages


def package_files(directory):
    """add package_files for setup."""
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


EXTRA_FILES = package_files('mapdesc/data')
SHORT_DESC = "Map Description and format conversion for robotics applications."


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="mapdesc",
    description=SHORT_DESC,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfki-ric/mapdesc",
    version="0.1",
    license="BSD-3",
    author="Andreas Bresser",
    packages=find_packages(),
    tests_require=[],
    include_package_data=True,
    package_data={'': EXTRA_FILES},
    install_requires=[
        'argcomplete',
        'jinja2',
        'pyyaml',
        'imutils',
        'numpy>=1.24',
        'OSMPythonTools'
    ],
    entry_points={
        'console_scripts': [
            'mapdesc = mapdesc.cli:main',
        ],
    },
)
