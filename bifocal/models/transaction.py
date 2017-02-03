# Copyright (c) 2013-2015, Vehbi Sinan Tunalioglu <vst@vsthost.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# (See http://opensource.org/licenses/BSD-2-Clause)


class Transaction:

    def __init__(self, timestamp, quantity, asset, **kwargs):
        self.quantity = quantity
        self.price = float(kwargs['price'] if 'price' in kwargs else None)
        self.timestamp = timestamp
        self.asset = asset
        self.data = kwargs

        if type(self.quantity) is not int:
            raise ValueError('Invalid quantity: %s' % self.quantity)
        if type(self.price) is not float:
            raise ValueError('Invalid price: %s' % self.price)
        if type(self.timestamp) is not int:
            raise ValueError('Invalid timestamp: %s' % self.timestamp)

    def __eq__(self, other):
        for key, value in self.data.iteritems():
            if key not in other.data:
                return False
            if value != other.data[key]:
                return False
        if self.quantity != other.quantity:
            return False
        if self.price != other.price:
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.asset != other.asset:
            return False
        return True

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return "%s: %s %s @ %s" % (
            self.timestamp,
            self.quantity,
            self.asset,
            self.price
        )

    def invert_quantity(self):
        self.quantity = self.quantity * -1

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

    def copy(self, quantity=None):
        return Transaction(
            self.timestamp,
            quantity or self.quantity,
            self.asset,
            **self.data
        )

    def finalize(self):
        pass
