# -*- coding: utf-8 -*-
# Copyright 2019 Christoph Wagner
#     https://www.tu-ilmenau.de/it-ems/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''Setup script for installing Picasso with pip'''

# import modules
import sys
import os
import re
from setuptools import setup

# global package constants
packageName     = 'EMSPicasso'
packageVersion  = '0.0.0'     #fallback version tag
picassoScript   = 'bin/picasso'
fullVersion     = packageVersion
strVersionFile  = "%s/version.py" %(packageName)

VERSION_PY = """
# -*- coding: utf-8 -*-
# This file carries the module's version information which will be updated
# during execution of the installation script, setup.py. Distribution tarballs
# contain a pre-generated copy of this file.

__version__ = '%s'
"""

##############################################################################
### function and class declaration section. DO NOT PUT SCRIPT CODE IN BETWEEN
##############################################################################

# determine requirements for install and setup
def checkRequirement(lstRequirements, importName, requirementName):
    '''
    Don't add packages unconditionally as this involves the risk of updating an
    already installed package. Sometimes this may break during install or mix
    up dependencies after install. Consider an update only if the requested
    package is not installed at all.
    '''
    try:
        __import__(importName)
    except ImportError:
        lstRequirements.append(requirementName)
    else:
        if 'bdist_wheel' in sys.argv[1:]:
            lstRequirements.append(requirementName)

def getCurrentVersion():
    '''
    Determine package version and put it in the signatures.
    '''
    global packageVersion
    global fullVersion

    # check if there is a manual version override
    if os.path.isfile(".version"):
        with open(".version", "r") as f:
            stdout = f.read().split('\n')[0]
        print("Override of version string to '%s' (from .version file )" % (
            stdout))

        fullVersion = stdout

    packageVersion = fullVersion


if __name__ == '__main__':
    # get version from git and update Picasso/__init__.py accordingly
    getCurrentVersion()

    # make sure there exists a version.py file in the project
    with open(strVersionFile, "w") as f:
        f.write(VERSION_PY % (fullVersion))
    print("Set %s to '%s'" % (strVersionFile, fullVersion))

    # get the long description from the README file.
    # CAUTION: Python2/3 utf encoding shit calls needs some adjustments
    fileName = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'README.md'
    )

    f = (open(fileName, 'r') if sys.version_info < (3, 0)
         else open(fileName, 'r', encoding='utf-8'))
    longDescription = f.read()
    f.close()

    print("Building %s v%s" % (
        packageName,
        packageVersion
    ))

    # check if all requirements are met prior to actually calling setup()
    setupRequires = []
    installRequires = []
    checkRequirement(setupRequires, 'setuptools', 'setuptools>=18.0')
    checkRequirement(installRequires, 'Pillow', 'Pillow>=4.0.0')
    checkRequirement(installRequires, 'numpy', 'numpy>=1.16.4')

    setup(
        name=packageName,
        version=packageVersion,
        description=('A tool to modify images.'),
        long_description=longDescription,
        author='Christoph Wagner, EMS Research Group TU Ilmenau',
        author_email='christoph.wagner@tu-ilmenau.de',
        url='https://github.com/EMS-TU-Ilmenau/Picasso',
        license='Apache Software License',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Version Control :: Git',
            'Topic :: Utilities'
        ],
        keywords=('image manipulation'),
        setup_requires=setupRequires,
        install_requires=installRequires,
        packages=[packageName],
        scripts=[picassoScript]
    )
