# -*- coding: utf-8 -*-
from setuptools import setup

import japanese_calendar

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="japanesecalendar",
    version=japanese_calendar.__version__,
    description="check if some day is holiday in Japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hack Fang",
    author_email="likai.fang@gmail.com",
    url="https://github.com/hack-fang/japanese-calendar",
    license="MIT License",
    packages=["japanese_calendar"],
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
