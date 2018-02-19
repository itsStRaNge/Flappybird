# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='DeepCaddog',
      packages=find_packages(),
      install_requires=[
          'pygame',
          'pyserial',
      ], entry_points={'console_scripts': [
              # Add the functions that should become binaries here
              'myhello = example_package.example_module:example_function', ],
      })
