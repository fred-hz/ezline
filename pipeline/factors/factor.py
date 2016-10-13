from pipeline.expression import (
    NumericalExpression,
    BadBinaryOperator,
    method_name_for_op,
    unary_op_name,
    is_comparison,
    NUMEXPR_MATH_FUNCS,
    UNARY_OPS
)
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


class Factor(Term):

    # Dynamically bind the Python magic functions with NumericalExpressions

    clsdict = locals()
    clsdict.update(
        {
            #method_name_for_op(op):
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
