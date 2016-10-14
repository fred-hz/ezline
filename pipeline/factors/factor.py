from pipeline.expression import (
    NumericalExpression,
    BadBinaryOperator,
    method_name_for_op,
    unary_op_name,
    is_comparison,
    NUMEXPR_MATH_FUNCS,
    UNARY_OPS,
    MATH_BINOPS,
    COMPARISONS
)
from numbers import Number
from operator import attrgetter
from pipeline.filters.filter import (
    NumExprFilter
)
from pipeline.term import Term


def binop_return_type(op):
    if is_comparison(op):
        return NumExprFilter
    else:
        return NumExprFactor


def binary_operator(op):
    """
    Factory function for making binary operator methods on a Factor subclass.
    Returns a function, "binary_operator" suitable for implementing functions
    like __add__.
    :param op:
    :return:
    """
    def _binary_operator(self, other):
        return_type = binop_return_type(op)
        if isinstance(self, NumExprFactor):
            self_expr, other_expr, new_inputs = self.build_binary_op(
                op, other
            )
            return return_type(
                "({left} {op} {right})".format(
                    left=self_expr,
                    op=op,
                    right=other_expr
                ),
                binds=new_inputs
            )
        elif isinstance(other, NumExprFactor):
            commuted_method_getter = attrgetter(method_name_for_op(op, commute=True))
            return commuted_method_getter(other)(self)
        elif isinstance(other, Term):
            if self is other:
                return return_type(
                    "x_0 {op} x_0".format(op=op),
                    binds=(self,)
                )
            return return_type(
                "x_0 {op} x_1".format(op=op),
                binds=(self, other)
            )
        elif isinstance(other, Number):
            return return_type(
                "x_0 {op} ({constant)".format(op=op, constant=other),
                binds=(self,)
            )
        raise BadBinaryOperator(op, self, other)
    return _binary_operator


def reflected_binary_operator(op):
    assert not is_comparison(op)

    def _reflected_binary_operator(self, other):
        if isinstance(self, NumericalExpression):
            self_expr, other_expr, new_inputs = self.build_binary_op(
                op, other
            )
            return NumExprFactor(
                "({left}) {op} ({right})".format(
                    left=other_expr,
                    right=self_expr,
                    op=op
                ),
                binds=new_inputs
            )
        elif isinstance(other, Number):
            return NumExprFactor(
                "{constant} {op} x_0".format(op=op, constant=other),
                binds=(self,)
            )
        raise BadBinaryOperator(op, other, self)
    return _reflected_binary_operator


def unary_operator(op):
    valid_ops = {'-'}
    if op not in valid_ops:
        raise ValueError("Invalid unary operator %s." % op)

    def _unary_operator(self):
        if isinstance(self, NumericalExpression):
            return NumExprFactor(
                "{op}({expr})".format(op=op, expr=self._expr),
                binds=self.inputs
            )
        else:
            return NumExprFactor(
                "{op}x_0".format(op=op),
                binds=(self,)
            )
    return _unary_operator


def function_application(func):
    if func not in NUMEXPR_MATH_FUNCS:
        raise ValueError("Unsupported mathematical function %s" % func)

    def mathfunc(self):
        if isinstance(self, NumericalExpression):
            return NumExprFactor(
                "{func}({expr})".format(func=func, expr=self._expr),
                binds=self.inputs
            )
        else:
            return NumExprFactor(
                "{func}(x_0)".format(func=func),
                binds=(self,)
            )
    return mathfunc


class Factor(Term):

    # Dynamically bind the Python magic functions with NumericalExpressions

    clsdict = locals()
    clsdict.update(
        {
            method_name_for_op(op): binary_operator(op)
            # Exclude __eq__ because actually it is the tuple to be compared
            for op in MATH_BINOPS.union(COMPARISONS - {'=='})
        }
    )
    clsdict.update(
        {
            method_name_for_op(op, commute=True): reflected_binary_operator(op)
            for op in MATH_BINOPS
        }
    )
    clsdict.update(
        {
            unary_op_name(op): unary_operator(op)
            for op in UNARY_OPS
        }
    )
    clsdict.update(
        {
            funcname: function_application(funcname)
            for funcname in NUMEXPR_MATH_FUNCS
        }
    )

    def _compute(self, inputs, time, assets, mask):
        pass


class NumExprFactor(NumericalExpression, Factor):
    """
    Factor computed from a numexpr expression

    Parameters
    ----------
    expr : string
        A string suitable for passing to numexpr. All variables
        in 'expr' will be in the form of 'x_i'
    binds : tuple
        A tuple of factors to use as inputs

    """
    pass
