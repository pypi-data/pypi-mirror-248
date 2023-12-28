#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of Python utility scripts for manipulating MS Outlook Calendar events.",
    entry_points={
        'console_scripts': [
            'clone-calendar-events=ms_outlook_calendar_utils.clone_calendar_events:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ms_outlook_calendar_utils',
    name='ms_outlook_calendar_utils',
    packages=find_packages(include=['ms_outlook_calendar_utils', 'ms_outlook_calendar_utils.*']),
    package_data={"ms_outlook_calendar_utils": [".env.example"]},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/ms_outlook_calendar_utils',
    version='0.1.0',
    zip_safe=False,
)
