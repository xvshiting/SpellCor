import os
import re
from distutils.command.build import build
from distutils.command.build_ext import build_ext
from setuptools.command.install import install
from distutils.spawn import find_executable
from distutils.version import LooseVersion
from setuptools import setup
from setuptools.extension import Extension
import subprocess

this_dir = os.path.dirname(os.path.abspath(__file__))


class CustomBuild(build):
    def run(self):
        self.run_command('build_ext')
        build.run(self)


class CustomInstall(install):
    def run(self):
        self.run_command('build_ext')
        install.run(self)

VERSION = '0.0.17'

setup(
    name='spellcor',
    version=VERSION,
    author='will xu',
    author_email='xvshiting@live.com',
    url='https://github.com/xvshiting/SpellCor',
    download_url='https://github.com/xvshiting/SpellCor' + VERSION,
    description='spell checker',
    long_description='context-based spell checker',
    keywords=['nlp', 'spell', 'spell-checker', 'spellcor'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    py_modules=['spellcor','spellcor_utils'],
    packages=['spellcor_models'],
    zip_safe=False,
    cmdclass={
        'build': CustomBuild,
        'install': CustomInstall,
    },
    include_package_data=True,
)