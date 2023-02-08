#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import io
import os

from uca.__version__ import __version__
from setuptools import setup, find_packages


# What packages are required for this module to be executed?
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIRED = f.read().splitlines()

PROJECT_URL = "https://github.com/Cloudzero/cloudzero-uca-tools"
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='cloudzero-uca-toolkit',
    version=__version__,
    description='CloudZero UCA Toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
    license="Apache-2.0",
    zip_safe=False,
    keywords='CloudZero UCA Toolkit unit cost analysis economics',
    platforms=['MacOS', 'Unix'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Unix'
    ],
)
