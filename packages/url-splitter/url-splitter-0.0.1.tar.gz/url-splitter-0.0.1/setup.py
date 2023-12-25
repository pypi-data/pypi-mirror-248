from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A basic URL splitter tool'
LONG_DESCRIPTION = 'A basic tool for Endpoint Splitting and output the data in a file.'

# Setting up
setup(
    name="url-splitter",
    version=VERSION,
    author="Thejas hari",
    author_email="<thejaskala308@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'url', 'url-splitter', 'endpoint splitter'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)