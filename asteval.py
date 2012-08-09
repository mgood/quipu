"""
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
"""

# we use floating-point division by default
from __future__ import division
import ast
import operator


class Evaluator(ast.NodeTransformer):
  default_context = {
    'True': True,
    'False': False,
  }

  @classmethod
  def evaluate(cls, expr, vars=None, funcs=None):
    """ Parse and evaluate an expression. """
    if vars is None:
      vars = {}
    if funcs is None:
      funcs = {}
    vars = dict(vars, **cls.default_context)
    tree = ast.parse(expr, mode='eval')
    return cls(vars, funcs).visit(tree)

  def __init__(self, variables, funcs):
    self.variables = variables
    self.funcs = funcs

  binary_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
    ast.BitAnd: operator.and_,
    ast.FloorDiv: operator.floordiv,
  }

  unary_ops = {
    ast.Invert: operator.invert,
    ast.Not: operator.not_,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
  }

  bool_ops = {
    ast.And: all,
    ast.Or: any,
  }

  compare_ops = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    # include Is and IsNot?
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
  }

  def find_operator(self, op_map, op):
    for op_type, op_func in op_map.iteritems():
      if isinstance(op, op_type):
        return op_func
    else:
      raise ValueError('Unknown operator: %s' % op)

  def visit_Expression(self, node):
    return self.visit(node.body)

  def visit_BinOp(self, node):
    op_func = self.find_operator(self.binary_ops, node.op)
    left = self.visit(node.left)
    right = self.visit(node.right)
    return op_func(left, right)

  def visit_UnaryOp(self, node):
    op_func = self.find_operator(self.unary_ops, node.op)
    return op_func(self.visit(node.operand))

  def visit_Compare(self, node):
    left = self.visit(node.left)
    for op_node, comp_node in zip(node.ops, node.comparators):
      op_func = self.find_operator(self.compare_ops, op_node)
      right = self.visit(comp_node)
      if not op_func(left, right):
        return False
      left = right
    return True

  def visit_Name(self, node):
    if not isinstance(node.ctx, ast.Load):
      raise ValueError('Can only read variables')
    try:
      return self.variables[node.id]
    except KeyError:
      raise ValueError('Unknown variable: %s' % node.id)

  def visit_BoolOp(self, node):
    op_func = self.find_operator(self.bool_ops, node.op)
    return op_func(self.visit(v) for v in node.values)

  def visit_Call(self, node):
    if not isinstance(node.func, ast.Name):
      raise ValueError()
    if not isinstance(node.func.ctx, ast.Load):
      raise ValueError('Can only read variables')

    try:
      func = self.funcs[node.func.id]
    except KeyError:
      raise ValueError()

    args = [self.visit(x) for x in node.args]
    return func(*args)

  def visit_IfExp(self, node):
    if self.visit(node.test):
      return self.visit(node.body)
    else:
      return self.visit(node.orelse)

  def visit_List(self, node):
    if not isinstance(node.ctx, ast.Load):
      raise ValueError('Can only read variables')
    return [self.visit(x) for x in node.elts]

  def visit_Tuple(self, node):
    if not isinstance(node.ctx, ast.Load):
      raise ValueError('Can only read variables')
    return tuple(self.visit(x) for x in node.elts)

  def visit_Num(self, node):
    return node.n

  def visit_Str(self, node):
    return node.s

  def generic_visit(self, node):
    raise ValueError('Unknown node type: %s' % node.__class__.__name__)


evaluate = Evaluator.evaluate
