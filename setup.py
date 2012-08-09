#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'quipu',
  version = '0.1',
  license = 'BSD',
  description = open('README.txt').read(),
  author = 'Matt Good',
  author_email = 'matt@matt-good.net',
  url = 'https://github.com/mgood/quipu',
  platforms = 'any',

  py_modules = ['quipu'],

  zip_safe = True,
  verbose = False,
)
