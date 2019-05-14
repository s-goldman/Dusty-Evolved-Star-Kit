#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'tqdm', 'scipy']

setup_requirements = ['numpy']

test_requirements = ['scipy']

setup(
    author="Steven R. Goldman",
    author_email='sgoldman@stsci.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="The DESK is an SED-fitting python scripts for fitting data from evolved stars",
    entry_points={'console_scripts': ['fit_sed = desk.sed_fit:main']},
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='Dusty_Evolved_Star_Kit',
    name='desk',
    packages=find_packages(include=['desk']),
    package_data={'project': ['desk/models/*', 'desk/put_target_data_here/*']},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/s-goldman/Dusty_Evolved_Star_Kit',
    version='1.4.9',
    zip_safe=False,
)
