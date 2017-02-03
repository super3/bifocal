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

import datetime
from collections import deque
from bifocal import utils
from bifocal.models import Transaction


class IFO(object):

    def __init__(self, transactions=[]):
        self._started_at = datetime.datetime.now()
        self._finished_at = None

        self._transactions = transactions

        self._balance = 0
        self.inventory = deque()
        self.trace = []
        self._gains = 0.0

        self._compute()

    @property
    def is_empty(self):
        return len(self.inventory) == 0

    @property
    def stock(self):
        return self._balance

    @property
    def valuation(self):
        return sum([s.quantity * s.price for s in self.inventory])

    @property
    def valuation_factored(self):
        return sum([s.quantity * s.price * s.factor for s in self.inventory])

    @property
    def avgcost(self):
        return None if self._balance == 0 else (self.valuation / self._balance)

    @property
    def avgcost_factored(self):
        if self._balance == 0:
            return None
        else:
            return (self.valuation_factored / self._balance)

    @property
    def runtime(self):
        if self._started_at is not None and self._finished_at is not None:
            return self._finished_at - self._started_at
        return None

    @property
    def gains(self):
        return self._gains

    def _push(self, transaction):
        self.inventory.append(transaction)
        self._balance += transaction.quantity

    def _compute(self):
        for transaction in [tx.copy() for tx in self._transactions]:
            if ((self._balance >= 0 and transaction.buy)
                    or (self._balance <= 0 and transaction.sell)):
                self._push(transaction)
            elif not transaction.zero:
                self._fill(transaction)

        self._finished_at = datetime.datetime.now()

    def __repr__(self):
        return (type(self).__name__ + ' accounting('
                + 'bal : %s  ' % self._balance
                + 'gain: %s  ' % self._gains
                + 'txns: %s  ' % len(self._transactions)
                + 'trce: %s  ' % len(self.trace)
                + ')  ')
