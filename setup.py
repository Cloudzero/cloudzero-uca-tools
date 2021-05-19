#!/usr/bin/env python
# Copyright (c) 2016-present, CloudZero, Inc. All rights reserved.
# Licensed under the BSD-style license. See LICENSE file in the project root for full license information.

import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Command, find_packages

from mypythonlib import __version__

# Package meta-data.
NAME = 'mypythonlib'
DESCRIPTION = 'Standard open source python library'
URL = 'https://github.com/Cloudzero/mypythonlib'
EMAIL = 'support@cloudzero.com'
AUTHOR = 'CloudZero'

here = os.path.abspath(os.path.dirname(__file__))

# What packages are required for this module to be executed?
with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIRED = f.read().splitlines()

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=['tests*']),

    install_requires=REQUIRED,
    include_package_data=True,
    license='BSD',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    # $ setup.py upload support.
    cmdclass={
        'upload': UploadCommand,
    },
)
