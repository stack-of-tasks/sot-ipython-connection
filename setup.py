#!/usr/bin/env python

from pathlib import Path
from setuptools import setup, find_packages

PACKAGE_NAME = "sot_ipython_connection"

setup(
    name=PACKAGE_NAME,
    version="1.0",
    description="",
    author="Justine Fricou",
    author_email="justine.fricou@gmail.com",
    packages=find_packages(where='src_python'),
    package_dir={PACKAGE_NAME: str(Path("src_python") / PACKAGE_NAME)},
)
    