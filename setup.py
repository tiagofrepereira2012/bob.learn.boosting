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

from setuptools import setup, find_packages, dist
dist.Distribution(dict(setup_requires='xbob.extension'))
from xbob.extension import Extension, build_ext

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    # This is the basic information about your project. Modify all this
    # information before releasing code publicly.
    name='xbob.boosting',
    version='1.0.1a0',
    description='Boosting framework for Bob',

    url='https://gitlab.idiap.ch/manuel.guenther/xbob-boosting',
    license='GPLv3',
    author='Rakesh Mehta',
    author_email='rakesh.mehta@idiap.ch',

    # If you have a better, long description of your package, place it on the
    # 'doc' directory and then hook it here
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,

    setup_requires=[
      'xbob.extension',
    ],

    # This line defines which packages should be installed when you "install"
    # this package. All packages that are mentioned here, but are not installed
    # on the current system will be installed locally and only visible to the
    # scripts of this package. Don't worry - You won't need adminstrative
    # privileges when using buildout.
    install_requires=[
      'setuptools',
      'bob', # base signal proc./machine learning library
    ],

    cmdclass={
      'build_ext': build_ext,
    },

    ext_modules = [
      Extension(
        'xbob.boosting._boosting',
        [
          "xbob/boosting/cpp/StumpMachine.cpp",
          "xbob/boosting/cpp/LUTMachine.cpp",
          "xbob/boosting/cpp/BoostedMachine.cpp",
          "xbob/boosting/cpp/bindings.cpp",
        ],
        pkgconfig = [
          'bob-io',
        ],
# STUFF for DEBUGGING goes here (requires DEBUG bob version...):
#        extra_compile_args = [
#          '-ggdb',
#        ],
#        define_macros = [
#          ('BZ_DEBUG', 1)
#        ],
#        undef_macros=[
#          'NDEBUG'
#        ]
      )
    ],

    # Your project should be called something like 'xbob.<foo>' or
    # 'xbob.<foo>.<bar>'. To implement this correctly and still get all your
    # packages to be imported w/o problems, you need to implement namespaces
    # on the various levels of the package and declare them here. See more
    # about this here:
    # http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
    #
    # Our database packages are good examples of namespace implementations
    # using several layers. You can check them out here:
    # https://github.com/idiap/bob/wiki/Satellite-Packages
    namespace_packages = [
      'xbob',
    ],

    # This entry defines which scripts you will have inside the 'bin' directory
    # once you install the package (or run 'bin/buildout'). The order of each
    # entry under 'console_scripts' is like this:
    #   script-name-at-bin-directory = module.at.your.library:function
    #
    # The module.at.your.library is the python file within your library, using
    # the python syntax for directories (i.e., a '.' instead of '/' or '\').
    # This syntax also omits the '.py' extension of the filename. So, a file
    # installed under 'example/foo.py' that contains a function which
    # implements the 'main()' function of particular script you want to have
    # should be referred as 'example.foo:main'.
    #
    # In this simple example we will create a single program that will print
    # the version of bob.
    entry_points={

      # scripts should be declared using this entry:
      'console_scripts': [
          'boosting_example.py = xbob.boosting.examples.mnist:main',
#          'mnist_binary_all.py = xbob.boosting.scripts.mnist_binary_all:main',
#          'mnist_binary_one.py = xbob.boosting.scripts.mnist_binary_one:main',
#          'mnist_multi.py = xbob.boosting.scripts.mnist_multi:main',
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
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
