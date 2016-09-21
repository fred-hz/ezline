class Transaction(object):

    def __init__(self, sid, amount, dt, price, order_id, commission=None):
        self.sid = sid
        self.amount = amount
        self.dt = dt
        self.price = price,
        self.order_id = order_id
        self.commission = commission
