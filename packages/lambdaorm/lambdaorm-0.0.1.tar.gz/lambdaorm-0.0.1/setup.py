#!/usr/bin/env python3
from setuptools import setup
# from distutils.core import setup
with open('README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(
  name = 'lambdaorm',
  packages = ['lambdaorm'],
  version = '0.0.1',
  license='MIT', 
  description = 'LambdaORM Client for Python',
  author = 'Flavio Lionel Rita',
  author_email = 'flaviolrita@proton.me',
  url = 'https://github.com/lambda-orm/lambdaorm-client-kotlin',
  download_url = 'https://github.com/lambda-orm/lambdaorm-client-kotlin',
  keywords = ['orm', 'lambdaorm', 'lambda', 'orm-client', 'orm-client-python'],
  install_requires=['dataclasses-json'],
  classifiers = []
)