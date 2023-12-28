# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="refractBatch",
    version="1.24.1",
    description="Batch prediction recipe",
    author="Amit Boke",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["refractml", "refractio[snowflake]"],
    # install_requires=[],
    python_requires=">=3.8,<3.10"
)
