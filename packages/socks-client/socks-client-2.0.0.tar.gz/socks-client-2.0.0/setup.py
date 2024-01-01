#!/usr/bin/env python
import os
import re

from setuptools import setup, find_packages

base_path = os.path.dirname(__file__)

with open(os.path.join(base_path, "README.md")) as f:
    long_description = f.read()

with open(os.path.join(base_path, "socks_client/__version__.py")) as f:
    pattern = r'__version__ = "(.*?)"'
    match = re.search(pattern, f.read())
    if match:
        VERSION = match.group(1)
    else:
        VERSION = None
    print(VERSION)


setup(
    name="socks-client",
    version=VERSION,

    description="Supports both TCP and UDP client with the implementation of SOCKS5 and SOCKS4 protocol",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author="Plattanus",
    author_email="plattanus@outlook.com",
    url="https://github.com/plattanus/socks-client",
    license="MIT License",
    keywords=["socks", "socks5", "socks4", "proxy", "asyncio", "tcp", "udp"],
    install_requires=[],
    python_requires=">=3.7",
    packages=[
        "socks_client",
    ],
)
