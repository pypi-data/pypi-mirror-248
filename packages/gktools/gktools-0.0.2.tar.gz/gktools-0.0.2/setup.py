from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'gktools is an assiting package for doing basic math operations'
LONG_DESCRIPTION = 'A package that allows to do basic math operations. This package is built as part of a tutorial for packaging python module'

# Setting up
setup(
    name="gktools",
    version=VERSION,
    author="Gokul Kumar Jayaram",
    author_email="<gokulkumar.jayaram@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'gktools', 'packaging' , 'baisc math'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)