import datetime
from collections import deque


class Transaction:

    def __init__(self, timestamp, quantity, price, asset):
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.asset = asset

    def __str__(self):
        return "%s: %s%s at %s" % (
            self.timestamp,
            self.quantity,
            self.price,
            self.asset
        )

    @property
    def size(self):
        return abs(self.quantity)

    @property
    def buy(self):
        return self.quantity > 0

    @property
    def sell(self):
        return self.quantity < 0

    @property
    def zero(self):
        return self.quantity == 0

    def copy(self, quantity=none):
        return Transaction(
            self.timestamp
            quantity or self.quantity,
            self.price,
            self.asset
        )
