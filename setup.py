#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Manuel Guenther <manuel.guenther@idiap.ch>
#Thu Feb 13 19:18:24 CET 2014
#
# This file contains the python (distutils/setuptools) instructions so your
# package can be installed on **any** host system. It defines some basic
# information like the package name for instance, or its homepage.
#
# It also defines which other packages this python package depends on and that
# are required for this package's operation. The python subsystem will make
# sure all dependent packages are installed or will install them for you upon
# the installation of this package.
#
# The 'buildout' system we use here will go further and wrap this package in
# such a way to create an isolated python working environment. Buildout will
# make sure that dependencies which are not yet installed do get installed, but
# **without** requiring adminstrative privileges on the host system. This
# allows you to test your package with new python dependencies w/o requiring
# administrative interventions.

bob_packages = ['bob.core', 'bob.io.base']

from setuptools import setup, find_packages, dist
dist.Distribution(dict(setup_requires=['bob.blitz'] + bob_packages))
from bob.blitz.extension import Extension, Library, build_ext

version = "2.0.0a0"

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    # This is the basic information about your project. Modify all this
    # information before releasing code publicly.
    name='bob.learn.boosting',
    version=version,
    description='Boosting framework for Bob',

    url='https://github.com/bioidiap/bob.learn.boosting',
    license='GPLv3',
    author='Manuel Guenther (with help of Rakesh Mehta)',
    author_email='manuel.guenther@idiap.ch',

    # If you have a better, long description of your package, place it on the
    # 'doc' directory and then hook it here
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,

    # This line defines which packages should be installed when you "install"
    # this package. All packages that are mentioned here, but are not installed
    # on the current system will be installed locally and only visible to the
    # scripts of this package. Don't worry - You won't need adminstrative
    # privileges when using buildout.
    install_requires=[
      'setuptools',
      'bob.extension',
      'bob.blitz',
      'bob.io.base',
#      'xbob.db.mnist' # for testing and the example
    ],

    # Declare that the package is in the namespace bob.learn
    namespace_packages = [
      'bob',
      'bob.learn'
    ],

    ext_modules = [
      Library(
        'bob.learn.boosting.bob_learn_boosting',
        [
          "bob/learn/boosting/cpp/LossFunction.cpp",
          "bob/learn/boosting/cpp/JesorskyLoss.cpp",

          "bob/learn/boosting/cpp/WeakMachine.cpp",
          "bob/learn/boosting/cpp/StumpMachine.cpp",
          "bob/learn/boosting/cpp/LUTMachine.cpp",
          "bob/learn/boosting/cpp/BoostedMachine.cpp",

          "bob/learn/boosting/cpp/LUTTrainer.cpp",
        ],
        bob_packages = bob_packages,
        version = version,
      ),

      Extension(
        'bob.learn.boosting._library',
        [
          "bob/learn/boosting/cpp/Bindings.cpp",
        ],
        bob_packages = bob_packages,
        version = version,
      ),
    ],

    # Declare that the package is in the namespace xbob
    namespace_packages = [
      'xbob',
    ],

    # Define the entry points for this package
    entry_points={

      # Console scripts, which will appear in ./bin/ after buildout
      'console_scripts': [
        'boosting_example.py = xbob.boosting.examples.mnist:main',
      ],

      # tests that are _exported_ (that can be executed by other packages) can
      # be signalized like this:
      'bob.test': [
        'boosting = xbob.boosting.tests.test_boosting:TestBoosting',
      ],

    },

    # Classifiers are important if you plan to distribute this package through
    # PyPI. You can find the complete list of classifiers that are valid and
    # useful here (http://pypi.python.org/pypi?%3Aaction=list_classifiers).
    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
