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

from unittest import TestCase

from bifocal.accounting import IFO, FIFO, LIFO
from bifocal.models import Transaction


class TestFIFO(TestCase):
    """
    Tests FIFO accounting.
    """

    def test_no_entries(self):
        """
        Tests the case that there are no entries.
        """
        fifo = FIFO()

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 0)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_single_buy(self):
        entries = [Transaction(0, 100, 'USD', price=10)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 1)
        self.assertFalse(fifo.is_empty)

        self.assertTrue(len(fifo.trace) == 0)

        self.assertTrue(fifo.stock, 100)

        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 10)

    def test_two_buys(self):
        entries = [Transaction(0, 100, 'USD', price=10),
                   Transaction(0, 100, 'USD', price=20)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 2)
        self.assertFalse(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 0)
        self.assertTrue(fifo.stock, 200)
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 15)

    def test_single_sell(self):
        entries = [Transaction(0, -100, 'USD', price=10)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 1)
        self.assertFalse(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 0)
        self.assertTrue(fifo.stock, -100)
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 10)

    def test_two_buys(self):
        entries = [Transaction(0, -100, 'USD', price=10),
                   Transaction(0, -100, 'USD', price=20)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 2)
        self.assertFalse(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 0)
        self.assertTrue(fifo.stock, -200)
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 15)

    def test_quick_square(self):
        entries = [Transaction(0, 100, 'USD', price=10),
                   Transaction(0, -100, 'USD', price=10)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 1)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_quick_alternate_square(self):
        entries = [Transaction(0, 100, 'USD', price=10),
                   Transaction(0, -100, 'USD', price=10)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 1)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_double_square(self):
        entries = [Transaction(0, 100, 'USD', price=10),
                   Transaction(0, -100, 'USD', price=10),
                   Transaction(0, 100, 'USD', price=10),
                   Transaction(0, -100, 'USD', price=10)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 2)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_double_alternate_square(self):
        entries = [Transaction(0, 100, 'USD', price=10),
                   Transaction(0, -100, 'USD', price=10),
                   Transaction(0, -100, 'USD', price=10),
                   Transaction(0, 100, 'USD', price=10)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 2)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_alternate_buy_sell(self):
        entries = [Transaction(0, 100, 'USD', price=10),
                   Transaction(0, -200, 'USD', price=10)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 1)
        self.assertFalse(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 1)
        self.assertEqual(fifo.stock, -100)
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 10)

    def test_alternate_sell_buy(self):
        entries = [Transaction(0, -100, 'USD', price=10),
                   Transaction(0, 200, 'USD', price=10)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 1)
        self.assertFalse(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 1)
        self.assertEqual(fifo.stock, 100)
        self.assertIsNotNone(fifo.avgcost)
        self.assertEqual(fifo.avgcost, 10)

    def test_multiple_Transaction_stock_out(self):
        entries = [Transaction(0, 100, 'USD', price=10),
                   Transaction(0, -50, 'USD', price=10),
                   Transaction(0, -50, 'USD', price=15)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 2)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_multiple_Transaction_stock_out_alt(self):
        entries = [Transaction(0, -100, 'USD', price=10),
                   Transaction(0, 50, 'USD', price=10),
                   Transaction(0, 50, 'USD', price=15)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 2)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_double_multiple_Transaction_stock_out(self):
        entries = [Transaction(0, 50, 'USD', price=10),
                   Transaction(0, 50, 'USD', price=12),
                   Transaction(0, -50, 'USD', price=10),
                   Transaction(0, -50, 'USD', price=15)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 2)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_double_multiple_Transaction_stock_out_alt(self):
        entries = [Transaction(0, 40, 'USD', price=10),
                   Transaction(0, 60, 'USD', price=12),
                   Transaction(0, -50, 'USD', price=10),
                   Transaction(0, -50, 'USD', price=15)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 3)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_double_multiple_Transaction_stock_out_alt2(self):
        entries = [Transaction(0, 60, 'USD', price=10),
                   Transaction(0, 40, 'USD', price=12),
                   Transaction(0, -50, 'USD', price=10),
                   Transaction(0, -50, 'USD', price=15)]

        fifo = FIFO(entries)

        self.assertTrue(len(fifo.inventory) == 0)
        self.assertTrue(fifo.is_empty)
        self.assertTrue(len(fifo.trace) == 3)
        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)

    def test_complex_trades(self):
        fifo = FIFO([Transaction(0, 60, 'USD', price=10),
                     Transaction(0, 10, 'USD', price=12),
                     Transaction(0, -50, 'USD', price=10)])
        self.assertEqual(fifo.stock, 20)
        self.assertEqual(fifo.avgcost, 11)

        fifo = FIFO([Transaction(0, 60, 'USD', price=10),
                     Transaction(0, 10, 'USD', price=12),
                     Transaction(0, -80, 'USD', price=10)])
        self.assertEqual(fifo.stock, -10)
        self.assertEqual(fifo.avgcost, 10)

        fifo = FIFO([Transaction(0, 60, 'USD', price=10),
                     Transaction(0, -10, 'USD', price=12),
                     Transaction(0, -20, 'USD', price=10),
                     Transaction(0, 50, 'USD', price=12),
                     Transaction(0, -60, 'USD', price=14),
                     Transaction(0, 10, 'USD', price=21)])

        self.assertEqual(fifo.stock, 30)
        self.assertEqual(fifo.avgcost, 15)

        fifo = FIFO([Transaction(0, 20, 'USD', price=10),
                     Transaction(0, 32, 'USD', price=7),
                     Transaction(0, 97, 'USD', price=6),
                     Transaction(0, 17, 'USD', price=2),
                     Transaction(0, 14, 'USD', price=0),
                     Transaction(0, -50, 'USD', price=9),
                     Transaction(0, -59, 'USD', price=6),
                     Transaction(0, -50, 'USD', price=8),
                     Transaction(0, 63, 'USD', price=10),
                     Transaction(0, -31, 'USD', price=6),
                     Transaction(0, -21, 'USD', price=1),
                     Transaction(0, -36, 'USD', price=10),
                     Transaction(0, -18, 'USD', price=2),
                     Transaction(0, 91, 'USD', price=2),
                     Transaction(0, 85, 'USD', price=4),
                     Transaction(0, -81, 'USD', price=1),
                     Transaction(0, 33, 'USD', price=2),
                     Transaction(0, 45, 'USD', price=4),
                     Transaction(0, -18, 'USD', price=4),
                     Transaction(0, -33, 'USD', price=7),
                     Transaction(0, -47, 'USD', price=3),
                     Transaction(0, -49, 'USD', price=7),
                     Transaction(0, 73, 'USD', price=3),
                     Transaction(0, 79, 'USD', price=10),
                     Transaction(0, 3, 'USD', price=5),
                     Transaction(0, 50, 'USD', price=7),
                     Transaction(0, -82, 'USD', price=10),
                     Transaction(0, 47, 'USD', price=9),
                     Transaction(0, 72, 'USD', price=10),
                     Transaction(0, 40, 'USD', price=1)])
        self.assertEqual(fifo.stock, 286)
        self.assertEqual(fifo.avgcost, 8)

        fifo = FIFO([Transaction(0, 20, 'USD', price=10),
                     Transaction(0, 32, 'USD', price=7),
                     Transaction(0, 97, 'USD', price=6),
                     Transaction(0, 17, 'USD', price=2),
                     Transaction(0, 14, 'USD', price=0),
                     Transaction(0, -50, 'USD', price=9),
                     Transaction(0, -59, 'USD', price=6),
                     Transaction(0, -50, 'USD', price=8),
                     Transaction(0, 63, 'USD', price=10),
                     Transaction(0, -31, 'USD', price=6),
                     Transaction(0, -21, 'USD', price=1),
                     Transaction(0, -36, 'USD', price=10),
                     Transaction(0, -18, 'USD', price=2),
                     Transaction(0, 91, 'USD', price=2),
                     Transaction(0, 85, 'USD', price=4),
                     Transaction(0, -81, 'USD', price=1),
                     Transaction(0, 33, 'USD', price=2),
                     Transaction(0, 45, 'USD', price=4),
                     Transaction(0, -18, 'USD', price=4),
                     Transaction(0, -33, 'USD', price=7),
                     Transaction(0, -47, 'USD', price=3),
                     Transaction(0, -49, 'USD', price=7),
                     Transaction(0, 73, 'USD', price=3),
                     Transaction(0, 79, 'USD', price=10),
                     Transaction(0, 3, 'USD', price=5),
                     Transaction(0, 50, 'USD', price=7),
                     Transaction(0, -82, 'USD', price=10),
                     Transaction(0, 47, 'USD', price=9),
                     Transaction(0, 72, 'USD', price=10),
                     Transaction(0, 40, 'USD', price=1),
                     Transaction(0, -286, 'USD', price=8)])

        self.assertEqual(fifo.stock, 0)
        self.assertIsNone(fifo.avgcost)
