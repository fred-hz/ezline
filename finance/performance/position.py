from collections import (
    OrderedDict,
    namedtuple
)

# Data structure for split_and_dividend input
SplitAndDividend = namedtuple('SplitAndDividend',
                              ['sid',
                               'per_cash_div',
                               'per_share_div_ratio',
                               'per_share_trans_ratio',
                               'allotment_ratio',
                               'allotment_price'])

class Position(object):

    def __init__(self, sid, amount=0, cost_basis=0.0,
                 last_sale_price=0.0, last_sale_date=None):
        self.sid = sid
        self.amount = amount
        self.cost_basis = cost_basis
        # Variables last_sale_price and last_sale_date will be synced every day
        self.last_sale_price = last_sale_price
        self.last_sale_date = last_sale_date

    def handle_split_and_dividend(self, sd):
        """
        :param sd: sd is short for splits and dividend. It's a namedtuple of
        (sid, div_date, per_cash_div, per_share_div_ratio,
        per_share_trans_ratio, allotment_ratio, allotment_price)
        :return:
        """
        sid = sd.sid
        if sid != self.sid:
            raise Exception('updating split and dividend with the wrong sid!')

        per_cash_div = sd.per_cash_div or 0.0
        per_share_div_ratio = sd.per_share_div_ratio or 0.0
        per_share_trans_ratio = sd.per_share_trans_ratio or 0.0
        allotment_ratio = sd.allotment_ratio or 0.0
        allotment_price = sd.allotment_price or 0.0

        self.amount *= 1 + per_share_div_ratio + per_share_trans_ratio + allotment_ratio
        self.cost_basis = (self.cost_basis + per_cash_div + allotment_price) / self.amount

    def update_transaction(self, txn):
        # Update a transaction
        if self.sid != txn.sid:
            raise Exception('updating transaction for position with the wrong sid!')

        total_share = self.amount + txn.amount

        if total_share == 0:
            self.cost_basis = 0.0
        else:
            # Not allowed to short stocks in the first place
            if txn.amount > 0:
                prev_cost = self.cost_basis * self.amount
                txn_cost = txn.price * txn.amount
                self.cost_basis = (prev_cost + txn_cost) / total_share

            if self.last_sale_date is None or txn.dt > self.last_sale_date:
                self.last_sale_date = txn.dt
                self.last_sale_price = txn.price

        self.amount = total_share

    def to_dict(self):
        return {
            'sid': self.sid,
            'amount': self.amount,
            'cost_basis': self.cost_basis,
            'last_sale_price': self.last_sale_price,
            'last_sale_date': self.last_sale_date,
        }


class PositionDict(OrderedDict):
    def __missing__(self, key):
        return None