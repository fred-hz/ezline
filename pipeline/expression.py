"""
NumericalExpression term, which is derived from the natural math operation of factors
"""
from numbers import Number
from .term import Term
from itertools import chain

import numexpr
from numpy import (
    full
)

# Map from op symbol to equivalent Python magic method name.
_ops_to_methods = {
    '+': '__add__',
    '-': '__sub__',
    '*': '__mul__',
    '/': '__div__',
    '%': '__mod__',
    '**': '__pow__',
    '&': '__and__',
    '|': '__or__',
    '^': '__xor__',
    '<': '__lt__',
    '<=': '__le__',
    '==': '__eq__',
    '!=': '__ne__',
    '>=': '__ge__',
    '>': '__gt__'
}
# Map from op symbol to equivalent Python magic method name after flipping
# arguments.
_ops_to_commuted_methods = {
    '+': '__radd__',
    '-': '__rsub__',
    '*': '__rmul__',
    '/': '__rdiv__',
    '%': '__rmod__',
    '**': '__rpow__',
    '&': '__rand__',
    '|': '__ror__',
    '^': '__rxor__',
    '<': '__gt__',
    '<=': '__ge__',
    '==': '__eq__',
    '!=': '__ne__',
    '>=': '__le__',
    '>': '__lt__',
}

_unary_ops_to_methods = {
    '-': '__neg__',
    '~': '__invert__'
}

UNARY_OPS = {'-'}
MATH_BINOPS = {'+', '-', '*', '/', '**', '%'}
FILTER_BINOPS = {'&', '|'}  # NumExpr doesn't support xor.
COMPARISONS = {'<', '<=', '!=', '>=', '>', '=='}

NUMEXPR_MATH_FUNCS = {
    'sin',
    'cos',
    'tan',
    'arcsin',
    'arccos',
    'arctan',
    'sinh',
    'cosh',
    'tanh',
    'arcsinh',
    'arccosh',
    'arctanh',
    'log',
    'log10',
    'log1p',
    'exp',
    'expm1',
    'sqrt',
    'abs',
}


def method_name_for_op(op, commute=False):
    """
    Get the name ofthe Python magic method of 'op'
    :param op:
    :param commute:
    :return:
    """
    if commute:
        return _ops_to_commuted_methods[op]
    return _ops_to_methods[op]


def unary_op_name(op):
    return _unary_ops_to_methods[op]


def is_comparison(op):
    return op in COMPARISONS


class BadBinaryOperator(TypeError):
    """
    Called when a bad binary operation is encountered.
    """
    def __init__(self, op, left, right):
        super(BadBinaryOperator, self).__init__(
            "Can't compute {left} {op} {right}".format(
                op=op,
                left=type(left).__name__,
                right=type(right).__name__
            )
        )


def _chain_tuple_element(tup, element):
    try:
        return tup, tup.index(element)
    except ValueError:
        return tuple(chain(tup, (element,))), len(tup)


class NumericalExpression(Term):
    def __init__(self, expr, inputs, window_length, missing_value):
        self._expr = expr
        self.inputs = inputs
        super(NumericalExpression, self).__init__(window_length, missing_value)

    def _compute(self, inputs, time, assets, mask):
        """
        Compute stored expression string with numexpr
        :param inputs:
        :param time:
        :param assets:
        :param mask:
        :return:
        """
        out = full(mask.shape, self.missing_value)
        numexpr.evaluate(
            self._expr,
            local_dict={
                "x_%d" % idx: array
                for idx, array in enumerate(inputs)
            },
            out=out
        )
        return out

    def _rebind_variables(self, new_inputs):
        """
        Rebind variables so that new expressions are generated. After such rebinding,
        the two NumercialExpression will be able to merge
        :param new_inputs:
        :return:
        """
        expr = self._expr

        # We need to interate the reversed inputs so that the replace action
        # won't be interwined by the case like x_1, x_10, x_100
        for idx, input_ in reversed(list(enumerate(self.inputs))):
            old_varname = "x_%d" % idx
            temp_new_varname = "x_temp_%d" % new_inputs.index(input_)
            expr = expr.replace(old_varname, temp_new_varname)

        return expr.replace("_temp_", "_")

    def _merge_experssions(self, other):
        """
        Merge the inputs of two NumericalExpressions into a single input tuple,
        rewriting their respective string expressions to make input names
        resolve correctly.
        Returns a tuple of (new_self_expr, new_other_expr, new_inputs)
        :param other:
        :return:
        """
        new_inputs = tuple(set(self.inputs).union(other.inputs))
        new_self_expr = self._rebind_variables(new_inputs)
        new_other_expr = self._rebind_variables(new_inputs)
        return new_self_expr, new_other_expr, new_inputs

    def build_binary_op(self, op, other):
        """
        Compute new expression strings and a new inputs tuple for combing self
        and other with a binary operator.
        :param op:
        :param other:
        :return:
        """
        if isinstance(other, NumericalExpression):
            self_expr, other_expr, new_inputs = self._merge_experssions(other)
        elif isinstance(other, Term):
            self_expr = self._expr
            new_inputs, other_idx = _chain_tuple_element(self.inputs, other)
            other_expr = "x_%d" % other_idx
        elif isinstance(other, Number):
            self_expr = self._expr
            other_expr = str(other)
            new_inputs = self.inputs
        else:
            raise BadBinaryOperator(op, other)

        return self_expr, other_expr, new_inputs

    @property
    def bindings(self):
        return {
            "x_%d" % i: input_
            for i, input_ in enumerate(self.inputs)
        }

    def __repr__(self):
        return "{typename}(expr='{expr}', bindings={bindings})".format(
            typename=type(self).__name__,
            expr=self._expr,
            bindings=self.bindings,
        )