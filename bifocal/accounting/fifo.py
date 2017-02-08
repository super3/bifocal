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

from ifo import IFO


class FIFO(IFO):

    def __init__(self, transactions=None):
        IFO.__init__(self, transactions)

    def _fill(self, transaction):
        transaction = transaction.copy()

        while not transaction.zero:
            if self.is_empty:
                self._push(transaction)
                return

            earliest = self.inventory.popleft()

            if transaction.size <= earliest.size:
                munched = earliest.copy(-transaction.quantity)

                earliest.quantity += transaction.quantity

                if earliest.quantity != 0:
                    self.inventory.appendleft(earliest)

                gain = munched.quantity * (transaction.price - munched.price)

                self.trace.append([munched, transaction, gain])

                self._balance += transaction.quantity
                self._gains += gain

                return
            else:
                munched = transaction.copy(-earliest.quantity)

                transaction.quantity += earliest.quantity

                gain = earliest.quantity * (munched.price - earliest.price)

                self.trace.append([earliest, munched, gain])

                self._balance += munched.quantity
                self._gains += gain
