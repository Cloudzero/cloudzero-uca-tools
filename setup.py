# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
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
    name='cloudzero-uca-tools',
    version=__version__,
    description='CloudZero UCA Tools',
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
    license="Proprietary",
    zip_safe=False,
    keywords='CloudZero UCA Tools',
    platforms=['MacOS', 'Unix'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Unix'
    ],
)
