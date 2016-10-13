from collections import namedtuple
from .position import (
    Position,
    PositionDict
)
from data.daily_trade import AshareDailyTrade

class PositionTracker(object):
    def __init__(self):
        self.positions = PositionDict()

    def update_position(self, sid, amount=None, last_sale_price=None,
                        last_sale_date=None, cost_basis=None):
        if sid not in self.positions:
            position = Position(sid)
            self.positions[sid] = position
        else:
            position = self.positions[sid]

        if amount is not None:
            position.amount = amount
        if last_sale_price is not None:
            position.last_sale_price = last_sale_price
        if last_sale_date is not None:
            position.last_sale_date = last_sale_date
        if cost_basis is not None:
            position.cost_basis = cost_basis

    def execute_transaction(self, txn):
        sid = txn.sid

        if sid not in self.positions:
            position = Position(sid)
            self.positions[sid] = position
        else:
            position = self.positions[sid]

        position.update_transaction(txn)
        if position.amount == 0:
            del self.positions[sid]

    def handle_commission(self, sid, cost):
        pass

    def handle_splits_and_dividend(self, sd_list):
        for sd in sd_list:
            sid = sd.sid
            if sid in self.positions.iterkeys():
                position = self.positions[sid]
                position.handle_split_and_dividend(sd)

    def sync_last_sale_prices(self, dt, ashare_data):
        # ashare_data is an instance of data.AshareDailyTrade
        for sid, position in self.positions.iteritems():
            if dt > position.last_sale_date:
                last_sale_price = ashare_data.get_trade_info(sid, dt, ['closePrice'])
                position.last_sale_date = dt
                position.last_sale_price = last_sale_price

    def get_positions_list(self):
        positions = []
        for pos in self.positions.itervalues():
            if pos.amount != 0:
                positions.append(pos.to_dict())
        return positions

    def get_value(self):
        total = 0
        for position in self.positions.itervalues():
            total += position.last_sale_price * position.amount
        return total
