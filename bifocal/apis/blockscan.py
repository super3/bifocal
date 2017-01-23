import requests
import json
from bifocal import utils, models
from polo import Polo
from coindesk import Coindesk


class Blockscan:

    def __init__(self):
        self._transactions = {}
        self._polo = Polo(None, None)
        self._coindesk = Coindesk()

    def _request(self, **kwargs):
        uri = 'http://xcp.blockscan.com/api2?%s' % utils.encode_args(kwargs)
        ret = requests.get(uri)
        return utils.parse_json(ret)

    def get_tx_by_id(self, txid):
        if txid not in self._transactions:
            self._transactions[txid] = self._request(
                module='transaction',
                action='info',
                txhash=txid
            )
        return self._transactions[txid]

    def get_address_transactions(self, address, asset):
        data = self._request(
            module='address',
            action='credit_debit',
            btc_address=address,
            asset=asset
        )
        transactions = data['data']
        return map(self._parse_tx, transactions)

    def get_tx_source(self, txid):
        tx = self.get_tx_by_id(txid)
        return tx['data'][0]['source']

    def get_tx_destination(self, txid):
        tx = self.get_tx_by_id(txid)
        return tx['data'][0]['destination']

    def _parse_tx(self, tx):
        sign = -1 if tx['type'] == 'DEBIT' else 1
        stamp = int(tx['block_time'])
        pair = "BTC_%s" % tx['asset']
        btc_rate = self._polo.get_daily_close_price(pair, stamp)
        return models.Transaction(
            timestamp=stamp,
            quantity=int(tx['quantity']) / 100000000 * sign,
            asset=tx['asset'],
            id=tx['event'],
            price=btc_rate * self._coindesk.get_price_by_timestamp(stamp),
            price_in_btc=btc_rate,
            source=self.get_tx_source(tx['event']),
            destination=self.get_tx_destination(tx['event'])
        )
