from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'Making Finance easy in Python!'
with open("pyfin_trading/README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="pyfin_trading",
    version=VERSION,
    author="Poonam Deshmukh",
    author_email="poonamdeshmukh616@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'finance', 'algorithmic trading', 'technical indicators'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)