#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bumpversion setup.cfg
"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

setup(
    author="Steven R. Goldman",
    author_email="sgoldman@stsci.edu",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="The DESK is an SED-fitting python scripts for fitting data from evolved stars",
    entry_points={"console_scripts": ["desk = desk.main:main"]},
    install_requires=[
        "astropy",
        "numpy",
        "scipy",
        "tqdm",
        "ipdb",
        "matplotlib",
        "sklearn",
        "h5py",
        "wheel",
        "twine",
        "sphinx",
        "sphinx_automodapi",
        "pytest-cov",
        "Pillow",
        "seaborn",
    ],
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="Dusty-Evolved-Star-Kit",
    name="desk",
    packages=find_packages(include=["desk"]),
    package_data={"project": ["desk/models/*", "desk/put_target_data_here/*"]},
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=["pytest", "sphinx_automodapi"],
    url="https://github.com/s-goldman/Dusty_Evolved_Star_Kit",
    version="1.8.4",
    zip_safe=False,
)
