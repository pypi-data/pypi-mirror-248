#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

from macaque import __description__
from macaque import __version__

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="macaque",
    version=f"{__version__}",
    keywords=["utx", "macaque", "monkey", "tools"],
    description=f"{__description__}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://github.com/openutx",
    author="lijiawei",
    author_email="jiawei.li2@qq.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console :: Curses",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points="""
    [console_scripts]
    macaque = macaque.__main__:prepare
    """,
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["airtest", "fire"],
)
