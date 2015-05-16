#!/usr/bin/python

"""libsaas gitlab
==========

Extension to libsaas library
"""
import os
from distutils.core import setup, Command
from setuptools import setup, find_packages

VERSION = (0, 3, 0, 'dev')

__version__   = ".".join(map(str, VERSION[0:3])) + "".join(VERSION[3:])
__author__    = "b-sh"
__contact__   = "b-sh@gmx.net"
__homepage__  = "http://github.com/bor-sh/libsaas_gitlab"
__docformat__ = "markdown"
__copyright__ = ""
__license__   = "BSD"

install_requires = ['libsaas==0.4']

class Test(Command):
    description = "run the automated test suite"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from test.run_tests import main
        if not main().wasSuccessful():
            raise SystemExit(1)

setup(name="libsaas_gitlab",
      version=__version__,
      description="",
      author=__author__,
      author_email=__contact__,
      url=__homepage__,
      license=__license__,
      packages=find_packages(),
      install_requires=install_requires,
      long_description=__doc__,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      platforms=["any"],
      cmdclass={'test': Test}
)
