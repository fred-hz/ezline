import uuid

# Create an order to exchange. If it is accepted, then transaction
class Order(object):
    def __init__(self, dt, sid, amount, id=None):
        self.id = id or self.make_id()
        self.dt = dt
        self.sid = sid
        self.amount = amount

    def make_id(self):
        return uuid.uuid4().hex