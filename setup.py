#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bumpversion setup.cfg
"""The setup script."""

from setuptools import setup, find_packages


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


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
    install_requires=["astropy", "numpy", "scipy", "tqdm", "ipdb"],
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="Dusty-Evolved-Star-Kit",
    name="desk",
    packages=find_packages(include=["desk"]),
    package_data={"project": ["desk/models/*", "desk/put_target_data_here/*"]},
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require="pytest",
    url="https://github.com/s-goldman/Dusty_Evolved_Star_Kit",
    version=get_version("package/__init__.py"),
    zip_safe=False,
)
