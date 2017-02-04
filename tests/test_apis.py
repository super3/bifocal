import json
import mock
from unittest import TestCase
from datetime import date

import bifocal


class TestBlocktrail(TestCase):

    def setUp(self):
        patcher = mock.patch('bifocal.apis.blocktrail.Coindesk')
        self.addCleanup(patcher.stop)
        self.mock_coindesk = patcher.start()

        with open('tests/blocktrail.json', 'rb') as jsonfile:
            self.test_json = json.loads(jsonfile.read())

        self.bt = bifocal.apis.Blocktrail('test')

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.bt._key, 'test')
        self.assertEqual(self.bt._chart,
                         self.mock_coindesk.get_chart.return_value)

    def test_request(self):
        pass

    def test_get_address_transactions(self):
        pass

    def test_parse_tx(self):
        self.bt._chart = {'2017-02-01': 5.3}
        tx = self.test_json['data'][0]

        expected_transactions = [
            bifocal.models.Transaction(
                timestamp=1485970539,
                quantity=8026276,
                asset='BTC',
                price=5.3,
                id=('3e811537c0aba45d7a06b42d4557f71b'
                    '0e2c58eca24a8df083acd09fca3f6736'),
                source='1B8xPwT33eb41C3osgVBJ8X11zFxZemQJ6',
                destination='1JtafJkuMTH21UD2M3MRQq2jZk8tSadz4U'),
        ]

        not_expected = [
            bifocal.models.Transaction(
                timestamp=1485970539,
                quantity=1772971,
                asset='BTC',
                price=5.3,
                id=('3e811537c0aba45d7a06b42d4557f71b'
                    '0e2c58eca24a8df083acd09fca3f6736'),
                source='1B8xPwT33eb41C3osgVBJ8X11zFxZemQJ6',
                destination='1DyGDUrmmXRp19K5zqJS6KQECZXESn9HMG'),
            bifocal.models.Transaction(
                timestamp=1485970539,
                quantity=25389,
                asset='BTC',
                price=5.3,
                id=('3e811537c0aba45d7a06b42d4557f71b'
                    '0e2c58eca24a8df083acd09fca3f6736'),
                source='1B8xPwT33eb41C3osgVBJ8X11zFxZemQJ6',
                destination='fee')
        ]

        transactions = self.bt._parse_tx(
            tx,
            '1JtafJkuMTH21UD2M3MRQq2jZk8tSadz4U')

        for tx in expected_transactions:
            self.assertIn(tx, transactions)

        for tx in not_expected:
            self.assertNotIn(tx, transactions)

    def test_clean_tx(self):
        tx = self.test_json['data'][0]
        expected_inputs = {
            '1B8xPwT33eb41C3osgVBJ8X11zFxZemQJ6': 9824636
        }
        expected_outputs = {
            '1JtafJkuMTH21UD2M3MRQq2jZk8tSadz4U': 8026276,
            '1DyGDUrmmXRp19K5zqJS6KQECZXESn9HMG': 1772971
        }

        inputs, outputs = self.bt._clean_tx(tx)

        self.assertEqual(inputs, expected_inputs)
        self.assertEqual(outputs, expected_outputs)

    def _get_bare_multisig(self):
        pass


class TestBlockscan(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_request(self):
        pass

    def test_get_tx_by_id(self):
        pass

    def test_get_address_transactions(self):
        pass

    def test_get_tx_source(self):
        pass

    def test_get_tx_destination(self):
        pass

    def test_parse_tx(self):
        pass


class TestCoindesk(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_chart(self):
        pass

    def test_get_date(self):
        pass

    def test_get_price_today(self):
        pass

    def test_get_price_by_date(self):
        pass

    def test_get_price_by_date_today(self):
        pass

    def test_get_price_by_timestamp(self):
        pass


class TestPolo(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        pass

    def test_make_public_request(self):
        pass

    def test_get_chart_data(self):
        pass

    def test_get_daily_close_price(self):
        pass

    def test_make_private_request(self):
        pass

    def test_get_trade_history(self):
        pass

    def test_parse_tx(self):
        pass

    def test_deposits_and_withdrawals(self):
        pass

    def test_get_deposits_and_withdrawals(self):
        pass

    def test_parse_deposit(self):
        pass

    def test_parse_withdrawal(self):
        pass
