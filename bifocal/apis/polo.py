import requests
import hmac
import hashlib
import time
from bifocal import utils


class Polo:

    def __init__(self, api_key, secret):
        self._api_key = api_key
        self._secret = secret
        self._charts = {}

    def _make_public_request(self, **kwargs):
        uri = 'https://poloniex.com/public?%s' % utils.encode_args(kwargs)
        ret = requests.get(uri)
        return utils.parse_json(ret)

    def _make_private_request(self, **kwargs):
        uri = 'https://poloniex.com/tradingApi'

        kwargs['nonce'] = int(time.time() * 1000)
        payload = utils.encode_args(kwargs)

        signature = hmac.new(self._secret, payload, hashlib.sha512).hexdigest()
        headers = {
            'Sign': signature,
            'Key': self._api_key
        }

        ret = requests.post(uri, data=kwargs, headers=headers)
        return utils.parse_json(ret)

    def get_trade_history(self, currency_pair):
        return self._make_private_request(
            command='returnTradeHistory',
            currencyPair=currency_pair
        )

    def _get_chart_data(self, currency_pair, start, end, period):
        return self._make_public_request(
            command='returnChartData',
            currencyPair=currency_pair,
            start=start,
            end=end,
            period=period
        )

    def _get_deposits_and_withdrawals(self, start, end):
        return self._make_private_request(
            command='returnDepositsWithdrawals',
            start=start,
            end=end
        )

    def get_daily_close_price(self, currency_pair, timestamp):
        timestamp = utils.timestamp_floor(timestamp)

        if currency_pair not in self._charts:
            self._charts[currency_pair] = self._get_chart_data(
                currency_pair,
                0,
                9999999999,
                86400
            )

        chart = self._charts[currency_pair]

        for row in chart:
            if row['date'] == timestamp:
                return float(row['close'])

        raise ValueError('No price found.')

    def get_deposit_addresses_by_asset(self, currency, start, end):
        addresses = []
        deposits = self._get_deposits_and_withdrawals(start, end)

        for deposit in deposits['deposits']:
            if deposit['currency'] == currency:
                if deposit['address'] not in addresses:
                    addresses.append(deposit['address'])

        return addresses
