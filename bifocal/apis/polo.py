import requests
import hmac
import hashlib
import time
from bifocal import utils, models
from coindesk import Coindesk


class Polo:

    def __init__(self, api_key, secret):
        self._api_key = api_key
        self._secret = secret
        self._charts = {}
        self._coindesk = Coindesk()

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
        history = self._make_private_request(
            command='returnTradeHistory',
            currencyPair=currency_pair,
            start=0,
            end=9999999999999
        )

        history = map(self._parse_tx, history)

        counter_trades = []
        for tx in history:
            tx.asset = currency_pair.split('_')[1]
            counter_trades.append(models.Transaction(
                quantity=tx.quantity * tx.data['price_in_btc'] * -1,
                asset=currency_pair.split('_')[0],
                id=tx.data['id'],
                timestamp=tx.timestamp,
                source='polo',
                destination='polo',
                price=self._coindesk.get_price_by_timestamp(tx.timestamp)
            ))

        return history, counter_trades

    def _parse_tx(self, tx):
        mod = -1 if tx['type'] == 'sell' else 1
        stamp = utils.date_to_timestamp(tx['date'], '%Y-%m-%d  %H:%M:%S')
        btc_price = float(tx['rate'])

        return models.Transaction(
            quantity=float(tx['amount']) * mod,
            asset=None,
            price=btc_price * self._coindesk.get_price_by_timestamp(stamp),
            id=tx['globalTradeID'],
            price_in_btc=btc_price,
            timestamp=stamp,
            source='polo',
            destionation='polo'
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
