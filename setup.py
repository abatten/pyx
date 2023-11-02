from setuptools import setup, find_packages
from codecs import open
import os
import re

with open("README.rst", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

def get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(here, 'pyx', '__version__.py')

    with open(version_file, "r") as vf:
        lines = vf.read()
        version = re.search(r"^_*version_* = ['\"]([^'\"]*)['\"]", lines, re.M).group(1)
        return version

setup(
    name='pyx',
    version=get_version(),
    author='Adam Batten',
    author_email='adamjbatten@gmail.com',
    url='https://github.com/abatten/pyx',
    description='A box of stuff',
    long_description=long_description,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        ],
    package_dir={"pyx": "pyx"},
    packages=find_packages(),
    include_package_data=True,
)
