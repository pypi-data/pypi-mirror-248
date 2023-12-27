#!/usr/bin/env python
# -*- coding: utf-8 -*-
# *****************************************************************************
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   See NOTICE file for details.
#
# *****************************************************************************
import sys
from pathlib import Path

from setuptools import Extension
from setuptools import setup

import setupext

if '--android' in sys.argv:
    platform = 'android'
    sys.argv.remove('--android')
else:
    platform = sys.platform


jpypeLib = Extension(name='_jpype', **setupext.platform.Platform(
    include_dirs=[Path('native', 'common', 'include'),
                  Path('native', 'python', 'include'),
                  Path('native', 'embedded', 'include')],
    sources=sorted(map(str, list(Path('native', 'common').glob('*.cpp')) +
             list(Path('native', 'python').glob('*.cpp')) +
             list(Path('native', 'embedded').glob('*.cpp')))), platform=platform,
))
jpypeJar = Extension(name="org.jpype",
                     sources=sorted(map(str, Path("native", "java").glob("**/*.java"))),
                     language="java",
                     libraries=["lib/asm-8.0.1.jar"]
                     )


setup(
    name='JPype1',
    version='1.5.0',
    description='A Python to Java bridge.',
    long_description=open('README.rst').read(),
    license='License :: OSI Approved :: Apache Software License',
    author='Steve Menard',
    author_email='devilwolf@users.sourceforge.net',
    maintainer='Luis Nell',
    maintainer_email='cooperate@originell.org',
    python_requires=">=3.7",
    url='https://github.com/jpype-project/jpype',
    platforms=[
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
    ],
    packages=['jpype', 'jpype._pyinstaller'],
    package_dir={'jpype': 'jpype', },
    package_data={'jpype': ['*.pyi']},
    install_requires=['typing_extensions ; python_version< "3.8"',
        'packaging'],
    tests_require=['pytest'],
    extras_require={
        'tests': [
            'pytest',
        ],
        'docs': [
            'readthedocs-sphinx-ext',
            'sphinx',
            'sphinx-rtd-theme',
        ],
    },
    cmdclass={
        'build_ext': setupext.build_ext.BuildExtCommand,
        'test_java': setupext.test_java.TestJavaCommand,
        'sdist': setupext.sdist.BuildSourceDistribution,
        'test': setupext.pytester.PyTest,
    },
    zip_safe=False,
    ext_modules=[jpypeJar, jpypeLib, ],
    distclass=setupext.dist.Distribution,
    entry_points={
        'pyinstaller40': [
            'hook-dirs = jpype._pyinstaller.entry_points:get_hook_dirs',
            'tests = jpype._pyinstaller.entry_points:get_PyInstaller_tests',
        ],
    },
)
