import requests
import json
from bifocal import utils


class Blockscan:

    def __init__(self):
        pass

    def _request(self, **kwargs):
        uri = 'http://xcp.blockscan.com/api2?%s' % utils.encode_args(kwargs)
        ret = requests.get(uri)
        return utils.parse_json(ret)

    def get_tx_by_id(self, txid):
        return self._request(
            module='transaction',
            action='info',
            txhash=txid
        )

    def get_address_transactions(self, address, asset):
        return self._request(
            module='address',
            action='credt_debit',
            btc_address=address,
            asset=asset
        )

    def get_source(self, txid):
        tx = self.get_tx_by_id(txid)
        return tx['data']['source']

    def get_destination(self, txid):
        tx = self.get_tx_by_id(txid)
        return tx['data']['destination']
