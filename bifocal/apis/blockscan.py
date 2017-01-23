import requests
import json
from bifocal import utils, models


class Blockscan:

    def __init__(self):
        self._transactions = {}

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
        transactions = data['txs']
        return map(self._parse_tx, transactions)

    def get_tx_source(self, txid):
        tx = self.get_tx_by_id(txid)
        return tx['data']['source']

    def get_tx_destination(self, txid):
        tx = self.get_tx_by_id(txid)
        return tx['data']['destination']

    def _parse_tx(self, tx):
        mod = -1 if tx['type'] == 'DEBIT' else 1
        return models.Transaction(
            timestamp=int(tx['timestamp']),
            quantity=mod * int(tx['quantity']) / 100000000,
            asset=tx['asset'],
            id=tx['event'],
            source=get_tx_source(tx['event']),
            destination=get_tx_destination(tx['event'])
        )
