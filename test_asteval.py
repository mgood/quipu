from __future__ import division

from nose.tools import eq_, assert_raises

from asteval import evaluate


supported_expressions = [
  '1',
  '-1',
  '2.5',
  '-(-1)',
  '+(1)',
  '~1',

  # strings
  '"text"',
  'u"foo"',

  # math
  '2 + 2',
  '10 - 5',
  '2 * 3',
  '20 / 2',
  '10 % 2',
  '3 ** 2',
  '8 << 1',
  '1 >> 8',
  '0b11 & 0b10',
  '0b10 | 0b01',
  '0b11 ^ 0b01',

  # uses "true" division by default
  '5 / 2',
  # use "//" for "floor" division
  '5 // 2',

  # function calls for whitelisted funcs
  'abs(-1)',
  'max([1, 2])',

  # variables
  'x * 2',
  '3 - -x',
  'x + 10 > y / 2',

  '1 == 1',
  '1 != 1',
  '1 < 2',
  '1 <= 2',
  '1 > 2',
  '1 >= 2',
  'x in (1, 2, 3)',
  'x not in (1, 2, 3)',
  'x in [1, 2, 3]',
  'x not in [1, 2, 3]',

  'x == y / 10',

  'True',
  'False',

  'not True',
  'not False',

  'True or False',
  'True and False',

  '1 if True else 2',
  '1 if False else 2',

  'x < 4 < 3',
  '(x < 4) < 3',
]
context = {'x': 2, 'y': 20, 'min': min}
funcs = {'abs': abs, 'max': max}

unsupported_expressions = [
  'import foo',

  # built-ins are not available
  'str',

  # foo is not in the context
  'foo',

  # min is a normal variable, not in the list of callable funcs
  'min([1, 2])',

  # don't allow attribute access
  'x.foo',
  'y.bar',

  # both sides of the comparison should be validated
  'x > y.foo',
  'x.foo > y',

  # both sides of bool op should be validated
  'False or bar',
  'foo or bar',
  'foo or True',

  'lambda: False',
  'if True: pass',
  'while True: pass',
  'for x in y: pass',

  # all 3 sections of if/else should be validated
  'foo if True else 1',
  '1 if False else foo',
  '1 if foo else 2',
]


def test_expressions():
  for expr in supported_expressions:
    yield check_supported, expr

  for expr in unsupported_expressions:
    yield check_unsupported, expr


def check_supported(expr):
  expected = eval(expr, funcs, context)
  eq_(expected, evaluate(expr, vars=context, funcs=funcs))


def check_unsupported(expr):
  # calls _validate_expression to make sure validation errors are raised
  # before trying to eval it
  assert_raises((ValueError, SyntaxError), evaluate, expr, vars=context, funcs=funcs)
