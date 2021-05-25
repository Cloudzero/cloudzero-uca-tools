# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import os

from uca import __version__
from setuptools import setup, find_packages


# What packages are required for this module to be executed?
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIRED = f.read().splitlines()

PROJECT_URL = "https://www.cloudzero.com"
doclink = "Please visit {}.".format(PROJECT_URL)

setup(
    name='uca',
    version=__version__,
    description='CloudZero UCA Tools',
    long_description=doclink,
    author='CloudZero',
    author_email='support@cloudzero.com',
    url=PROJECT_URL,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['uca=uca.main:cli']
    },
    package_data={'uca': ['data/*']},
    include_package_data=True,
    install_requires=REQUIRED,
    license="Proprietary",
    zip_safe=False,
    keywords='CloudZero UCA Tools',
    platforms=['MacOS', 'Unix'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Unix'
    ],
)
