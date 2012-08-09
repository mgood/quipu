asteval
=======

Evaluate simple Python expressions

An attempt to make a safe evaluator of a subset of Python expressions.

This is mostly a proof-of-concept for getting feedback, it has not been
thoroughly checked for safety, use at your own risk :)

It uses the Python ast module to parse the expression, but all evaluation is
done by walking the ast, it is not directly executed by the Python runtime.

Nosetests are provided below including coverage of supported and unsupported
operations.

Known security considerations:

The variables are expected to be simple primitive types. Providing functions
with unsafe effects, or variables where the operator implementations can have
unsafe effects is obviously unsafe.

Some operations may also take a lot of time or memory and DOS the process. 

Usage::

  import asteval
  result = asteval.evaluate('2 + 2')


See the list of "supported_expressions" in ``test_asteval.py`` for an example of
what operations are implemented.
