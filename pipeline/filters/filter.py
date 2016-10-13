from pipeline.expression import (
    BadBinaryOperator,
    FILTER_BINOPS,
    method_name_for_op,
    NumericalExpression
)
from pipeline.term import Term


class Filter(Term):
    def _compute(self, inputs, time, assets, mask):
        pass


class NumExprFilter(NumericalExpression, Filter):
    pass