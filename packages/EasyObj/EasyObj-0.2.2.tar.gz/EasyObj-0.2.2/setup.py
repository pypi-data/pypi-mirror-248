from setuptools import setup
from setuptools import find_packages

VERSION = '0.2.2'

setup(
    name='EasyObj',
    version=VERSION,
    description='A js-like object for python',
    packages=["EasyObj"],
    zip_safe=False,
    python_requires=">=3.8"
)
