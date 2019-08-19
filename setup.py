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

# import modules
import sys
import os
from setuptools import setup

# global package constants
packageName     = 'EMS-Picasso'
picassoScript    = 'bin/picasso'
if sys.version_info < (3, 0):
    # python 2
    import imp
    picasso = imp.load_source('picasso', picassoScript)
elif sys.version_info < (3, 3):
    # python 3.0 and up
    from importlib.machinery import SourceFileLoader
    picasso = SourceFileLoader('picasso', picassoScript).load_module()
else:
    # python 3.3 and up
    import importlib.util
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader('picasso', picassoScript)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    picasso = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(picasso)

packageVersion  = picasso.__version__


if __name__ == '__main__':
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
        author='Christoph Wagner, EMS Research Group TU Ilmenau',
        author_email='christoph.wagner@tu-ilmenau.de',
        url='https://ems-tu-ilmenau.github.io/Picasso/',
        license='Apache Software License',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Version Control :: Git',
            'Topic :: System :: Archiving :: Backup',
            'Topic :: System :: Archiving :: Mirroring',
            'Topic :: Utilities'
        ],
        keywords=('image manipulation'),
        setup_requires=setupRequires,
        install_requires=installRequires,
        scripts=['bin/picasso']
    )
