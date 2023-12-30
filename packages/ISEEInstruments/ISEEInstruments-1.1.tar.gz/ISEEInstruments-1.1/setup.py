# -*- coding: utf-8 -*-
"""
setup.py

Created on Tue Nov 22 09:40:02 2022

@author: Tyler
"""

import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

name = 'ISEEInstruments'
version = '1.01'
description = 'Data processing library for ISEE'
long_description = long_description
long_description_content_type = "text/markdown"
author = 'Steven Tyler King'
author_email = 'king.steven@stonybrook.edu'
url = r'https://bitbucket.org/takeuchimarschilok/instruments/src/master/'
classifiers=(
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent")
package_dir={'':"src"},
packages=find_packages("src"),
python_requires=">=3.6"
    
install_requires = [
    'numpy',
    'matplotlib',
    'scipy',
    'xlrd',
    'pymatgen',
    'sklearn']

setup(name=name,version=version,description=description,author=author,author_email=author_email,url=url)