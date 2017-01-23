import models
import apis
import accounting
import utils


class Bifocal:

    def __init__(self, addresses=[], assets=[],
                 polo_key=None, polo_secret=None):

        self._polo = apis.Polo(polo_key, polo_secret)
        self._blockscan = apis.Blockscan()
        self._blockchain = apis.Blockchain()

        self._assets = assets
        self._transaction_lists = {}
        for asset in self._assets:
            self._transaction_lists[asset] = []
        self.results = {}

        self.wallet = models.Wallet(addresses)

        self.make_transaction_lists()
        self.make_asset_results()

    def _add_addresses(self, addresses):
        self._addresses += set(addresses) - set(self._addresses)

    def _add_exchange_sales(self):
        self._add_polo_sales()

    def _add_polo_sales(self):
        for asset in self._assets:
            if asset != 'BTC':
                # assumes all non-btc assets are paired to BTC
                txs, counter_txs = self._polo.get_trade_history('BTC_' + asset)
                self._transaction_lists[asset] += txs
                self._transaction_lists['BTC'] += counter_txs

    def make_transaction_lists(self):
        for asset in self._assets:
            if asset != 'BTC':
                self._transaction_lists[asset] += utils.flatten(map(
                    (lambda a:
                     self._blockscan.get_address_transactions(a, asset)),
                    self.wallet
                ))
        self._transaction_lists['BTC'] += utils.flatten(map(
            lambda a: self._blockchain.get_address_transactions(a),
            self.wallet
        ))
        self._add_exchange_sales()
        self._filter_transactions()
        self._sort_transactions()

    def _sort_transactions(self):
        for asset in self._transaction_lists:
            self._transaction_lists[asset] = sorted(
                self._transaction_lists[asset],
                key=lambda k: k.timestamp
            )

    def _filter_transactions(self):
        for asset in self._transaction_lists:
            self._transaction_lists[asset] = filter(
                self._tx_filter,
                self._transaction_lists[asset]
            )

    def _tx_filter(self, tx):
        if tx.data['source'] in self.wallet:
            return True
        if tx.data['destination'] in self.wallet:
            return True
        if tx.data['destination'] == 'polo' or tx.data['source'] == 'polo':
            return True
        return False

    def make_asset_results(self):
        for asset in self._assets:
            self.results[asset] = {
                'FIFO': accounting.FIFO(self._transaction_lists[asset]),
                'LIFO': accounting.LIFO(self._transaction_lists[asset])
            }
