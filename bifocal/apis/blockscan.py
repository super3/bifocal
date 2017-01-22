import requests
import json
from bifocal import utils


class Blockscan:

    def __init__(self):
        self._transactions = {}
        pass

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
        return self._request(
            module='address',
            action='credt_debit',
            btc_address=address,
            asset=asset
        )

    def get_tx_source(self, txid):
        tx = self.get_tx_by_id(txid)
        return tx['data']['source']

    def get_tx_destination(self, txid):
        tx = self.get_tx_by_id(txid)
        return tx['data']['destination']
