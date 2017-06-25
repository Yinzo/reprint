# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="reprint",
    version="0.3.0",
    packages=find_packages(),
    install_requires=['six', 'backports.shutil_get_terminal_size'],
    author="Yinzo",
    author_email="oop995+pypi@gmail.com",
    description="A simple module for Python2/3 to print and refresh multi line output contents in terminal",
    license="Apache-2.0",
    keywords="multi line print value binding refresh",
    url="https://github.com/Yinzo/reprint",
)
