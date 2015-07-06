import sys, platform

if sys.version_info < (2, 4):
    print >> sys.stderr, "ERROR: bx-python requires python 2.4 or greater"
    sys.exit()

# Automatically download setuptools if not available
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import *
from glob import glob

try:
    import numpy
    have_numpy = True
except:
    have_numpy = False
       
def main():
    setup(  name = "joshua",
            version = "0.1",
            packages = find_packages( 'joshua' ),
            package_dir = { '': 'joshua' },
            package_data = { '': ['*.ps'] },
            scripts = glob( "scripts/*.py" ),
            ext_modules = get_extension_modules(),
            test_suite = 'nose.collector',
            setup_requires = ['nose>=0.10.4'],
            author = "Camille Scott, James Taylor, Bob Harris, David King, Brent Pedersen, Kanwei Li, and others",
            author_email = "camille.scott.w@gmail.com",
            description = "Fast interval tree implementation",
            #url = "http://bitbucket.org/james_taylor/bx-python/wiki/Home",
            license = "MIT",
            classifiers = [
                "Development Status :: 5 - Production/Stable",
                "Intended Audience :: Developers",
                "Intended Audience :: Science/Research",
                "License :: OSI Approved :: MIT License",
                "Operating System :: POSIX",
                "Programming Language :: Python :: 2",
                "Topic :: Scientific/Engineering :: Bio-Informatics",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
            zip_safe = False,
            dependency_links = [],
            cmdclass=command_classes )

# ---- Commands -------------------------------------------------------------

from distutils.core import Command

# Use build_ext from Cython
command_classes = {}

# Use build_ext from Cython if found
try:
    import Cython.Distutils
    command_classes['build_ext'] = Cython.Distutils.build_ext
except:
    pass

# Run 2to3 builder if we're on Python 3.x, from
#   http://wiki.python.org/moin/PortingPythonToPy3k
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    # 2.x
    from distutils.command.build_py import build_py
command_classes['build_py'] = build_py

# Use epydoc if found
try:
    import pkg_resources
    pkg_resources.require( "epydoc" )
    import epydoc.cli, sys, os, os.path
    # Create command class to build API documentation
    class BuildAPIDocs( Command ):
        user_options = []
        def initialize_options( self ):
            pass
        def finalize_options( self ):
            pass
        def run( self ):
            # Save working directory and args
            old_argv = sys.argv
            old_cwd = os.getcwd()
            # Build command line for Epydoc
            sys.argv = """epydoc.py bx --verbose --html --simple-term
                                       --exclude=._
                                       --exclude=_tests
                                       --docformat=reStructuredText
                                       --output=../doc/docbuild/html/apidoc""".split()
            # Make output directory
            if not os.path.exists( "./doc/docbuild/html/apidoc" ):
                os.mkdir( "./doc/docbuild/html/apidoc" )
            # Move to lib directory (so bx package is in current directory)
            os.chdir( "./joshua" )
            # Invoke epydoc
            epydoc.cli.cli()
            # Restore args and working directory
            sys.argv = old_argv
            os.chdir( old_cwd )
    # Add to extra_commands    
    command_classes['build_apidocs'] = BuildAPIDocs
except:
    pass

# ---- Extension Modules ----------------------------------------------------

def get_extension_modules():
    extensions = []

    extensions.append( Extension( "joshua.intervaltree", [ "joshua/intervaltree.pyx" ] ) )
    
    return extensions     
     
# ---- Monkey patches -------------------------------------------------------

def monkey_patch_doctest():
    #
    # Doctest and coverage don't get along, so we need to create
    # a monkeypatch that will replace the part of doctest that
    # interferes with coverage reports.
    #
    # The monkeypatch is based on this zope patch:
    # http://svn.zope.org/Zope3/trunk/src/zope/testing/doctest.py?rev=28679&r1=28703&r2=28705
    #
    try:
        import doctest
        _orp = doctest._OutputRedirectingPdb
        class NoseOutputRedirectingPdb(_orp):
            def __init__(self, out):
                self.__debugger_used = False
                _orp.__init__(self, out)

            def set_trace(self):
                self.__debugger_used = True
                _orp.set_trace(self)

            def set_continue(self):
                # Calling set_continue unconditionally would break unit test coverage
                # reporting, as Bdb.set_continue calls sys.settrace(None).
                if self.__debugger_used:
                    _orp.set_continue(self)
        doctest._OutputRedirectingPdb = NoseOutputRedirectingPdb
    except:
        pass

def monkey_patch_numpy():
    # Numpy pushes its tests into every importers namespace, yeccch.
    try:
        import numpy
        numpy.test = None
    except:
        pass
        
if __name__ == "__main__":
    monkey_patch_doctest()
    if have_numpy:
        monkey_patch_numpy()
    main()
