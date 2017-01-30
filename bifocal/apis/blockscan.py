import requests
from bifocal import utils, models
from polo import Polo
from coindesk import Coindesk


class Blockscan:

    @staticmethod
    def _request(**kwargs):
        uri = 'http://xcp.blockscan.com/api2?%s' % utils.encode_args(kwargs)
        ret = requests.get(uri)
        return utils.parse_json(ret)

    @staticmethod
    def get_tx_by_id(txid):
        return Blockscan._request(
            module='transaction',
            action='info',
            txhash=txid
        )

    @staticmethod
    def get_address_transactions(address, asset):
        data = Blockscan._request(
            module='address',
            action='credit_debit',
            btc_address=address,
            asset=asset
        )
        transactions = data['data']
        return map(Blockscan._parse_tx, transactions)

    @staticmethod
    def get_tx_source(txid):
        tx = get_tx_by_id(txid)
        return tx['data'][0]['source']

    @staticmethod
    def get_tx_destination(txid):
        tx = get_tx_by_id(txid)
        return tx['data'][0]['destination']

    @staticmethod
    def _parse_tx(tx):
        stamp = int(tx['block_time'])
        pair = "BTC_%s" % tx['asset']
        btc_rate = Polo.get_daily_close_price(pair, stamp)
        return models.Transaction(
            timestamp=stamp,
            quantity=int(tx['quantity']),
            asset=tx['asset'],
            id=tx['event'],
            price=btc_rate * Coindesk.get_price_by_timestamp(stamp),
            price_in_btc=btc_rate,
            source=Blockscan.get_tx_source(tx['event']),
            destination=Blockscan.get_tx_destination(tx['event'])
        )
