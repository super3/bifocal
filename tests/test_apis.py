from unittest import TestCase
import mock

import bifocal


class TestBlocktrail(TestCase):

    def setUp(self):
        patcher = mock.patch('bifocal.apis.blocktrail.Coindesk')
        self.addCleanup(patcher.stop)
        self.mock_coindesk = patcher.start()

        self.bt = bifocal.apis.Blocktrail('test')

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.bt._key, 'test')
        self.assertEqual(self.bt._chart,
                         self.mock_coindesk.get_chart.return_value)

    @mock.patch('bifocal.apis.blocktrail.utils')
    @mock.patch('bifocal.apis.blocktrail.requests')
    def test_request(self, mock_requests, mock_utils):
        route = 'addresses'
        kwargs = {
            'nonce': '17',
            'test': 'yes'
        }

        ret = '{"return": "certainly"}'
        mock_requests.get.return_value = ret
        encoded_kwargs = 'return=certainly'
        mock_utils.encode_args.return_value = encoded_kwargs

        self.bt._request(route, **kwargs)

        uri = ('https://api.blocktrail.com/v1/btc/%s?api_key=%s&%s'
               % (route, self.bt._key, encoded_kwargs))

        mock_utils.encode_args.assert_called_with(kwargs)
        mock_requests.get.assert_called_with(uri)
        mock_utils.parse_json.assert_called_with(ret)

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
