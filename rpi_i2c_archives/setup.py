import re
from os import path

from codecs import open  # To use a consistent encoding
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    with open('pyi2c/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


setup(name='pyi2c',
      version=get_version(),
      description='i2c communication for python',
      long_description=long_description,
      author='Daiem Ali',
      author_email='daiem.dna@gmail.com',
      include_package_data=True,
      license='FreeBSD',
      zip_safe=False,
      install_requires=['smbus2'],
      extras_require={
          'dev': [
              'pytest',
              'pytest-pep8',
              'pytest-cov',
          ]
      },
      classifiers=[
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6", ],
packages=find_packages())