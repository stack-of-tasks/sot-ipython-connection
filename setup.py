#!/usr/bin/env python

from pathlib import Path
from setuptools import setup

PACKAGE_NAME = "sot_ipython_connection"

setup(
    name=PACKAGE_NAME,
    version="1.0",
    description="",
    author="Justine Fricou",
    author_email="justine.fricou@gmail.com",
    package_dir={PACKAGE_NAME: str(Path("src_python") / PACKAGE_NAME)},
    packages=[PACKAGE_NAME],
)
