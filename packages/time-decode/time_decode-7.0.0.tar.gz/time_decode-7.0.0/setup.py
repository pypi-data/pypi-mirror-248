#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="time_decode",
    version="7.0.0",
    author="Corey Forman",
    license="MIT",
    url="https://github.com/digitalsleuth/time_decode",
    description=("Python 3 timestamp decode/encode tool"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "PyQt6",
        "python-dateutil",
        "colorama"
    ],
    entry_points={
        'console_scripts': [
            'time-decode = time_decode.time_decode:main'
        ]
    },
    package_data={'': ['README.md, LICENSE, REFERENCES.md']}
)
