#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'asteval',
  version = '0.1',
  license = 'BSD',
  description = open('README.txt').read(),
  author = 'Matt Good',
  author_email = 'matt@matt-good.net',
  url = 'https://github.com/mgood/asteval',
  platforms = 'any',

  py_modules = ['asteval'],

  zip_safe = True,
  verbose = False,
)
