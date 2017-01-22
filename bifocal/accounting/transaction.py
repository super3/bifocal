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

    def __init__(self, timestamp, quantity, price, asset):
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp
        self.asset = asset

    def __repr__(self):
        return "%s: %s %s @ %s" % (
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

    def copy(self, quantity=None):
        return Transaction(
            self.timestamp,
            quantity or self.quantity,
            self.price,
            self.asset
        )
