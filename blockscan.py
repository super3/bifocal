import requests
import json
import utils


class blockscan:

    def __init__(self):
        pass

    def _request(self, **kwargs):
        uri = 'https://counterpartychain.io/api/%s' % utils.encode_args(kwargs)
        ret = requests.get(uri)
        return utils.parse_json(ret)

    def _get_tx_by_id(self, txid):
        return _request(
            module='transaction',
            action='info',
            txhash=txid
        )

    def get_address_transactions(self, address, asset):
        return _request(
            module='address',
            action='credt_debit',
            btc_address=address,
            asset=asset
        )

    def get_source(self, txid):
        pass

    def get_destination(self, txid):
        pass
