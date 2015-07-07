import sys, platform

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

# Automatically download setuptools if not available
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import *
from glob import glob

if sys.version_info < (2, 4):
    print >> sys.stderr, "ERROR: joshua requires python 2.4 or greater"
    sys.exit()

try:
    import numpy
    have_numpy = True
except:
    have_numpy = False

cmdclass = {}
 
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
            cmdclass = cmdclass)

def get_extension_modules():
    extensions = []
    
    if use_cython:
        ext = '.pyx'
        cmdclass.update({ 'build_ext': build_ext })
    else:
        ext = '.c'

    extensions.append( Extension( "joshua.intervaltree", [ "joshua/intervaltree.pyx" ] ) )
    extensions.append( Extension( "joshua.utils", [ "joshua/utils.pyx" ] ) )

    return extensions     

def monkey_patch_numpy():
    # Numpy pushes its tests into every importers namespace, yeccch.
    try:
        import numpy
        numpy.test = None
    except:
        pass
        
if __name__ == "__main__":
    if have_numpy:
        monkey_patch_numpy()
    main()
