from unittest import TestCase
import mock

from bifocal import apis, utils


class TestBlocktrail(TestCase):

    def setUp(self):
        self.blocktrail = apis.Blocktrail('test')

    def tearDown(self):
        pass

    def test_init(self):
        pass

    def test_request(self):
        pass

    def test_get_address_transactions(self):
        pass

    def test_parse_tx(self):
        pass

    def test_clean_tx(self):
        pass

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
