import models
import apis
import accounting
import utils

# TODO: Get Polo deposit/withdrawals.
# Crawl transactions and filter out those ones by txid


class Bifocal:

    def __init__(self, wallets={}, polo_key=None, polo_secret=None):
        self._transaction_lists = {}
        self.wallets = wallets

        self._polo = apis.Polo(polo_key, polo_secret)

        for asset in self.wallets:
            self._transaction_lists[asset] = []
            self.wallets[asset] = models.Wallet(self.wallets[asset])
        self.results = {}

        self.make_transaction_lists()
        self.make_asset_results()

    def _add_addresses(self, addresses, asset):
        self.wallets[asset] += set(addresses) - set(self.wallets[asset])

    def _add_exchange_sales(self):
        self._add_polo_sales()

    def _add_polo_sales(self):
        for asset in self.wallet:
            if asset != 'BTC':
                # assumes all non-btc assets are paired to BTC
                txs, counter_txs = self._polo.get_trade_history('BTC_' + asset)
                self._transaction_lists[asset] += txs
                self._transaction_lists['BTC'] += counter_txs

    def make_transaction_lists(self):
        for asset in self.wallets:
            if asset != 'BTC':
                self._transaction_lists[asset] += utils.flatten(map(
                    (lambda a:
                     Blockscan.get_address_transactions(a, asset)),
                    self.wallets[asset]
                ))
        self._transaction_lists['BTC'] += utils.flatten(map(
            lambda a: Blockchain.get_address_transactions(a),
            self.wallets[asset]
        ))
        self._add_exchange_sales()
        self._filter_transactions()
        self._sort_transactions()

    def _sort_transactions(self):
        for asset in self.wallets:
            self._transaction_lists[asset] = sorted(
                self._transaction_lists[asset],
                key=lambda k: k.timestamp
            )

    def _filter_transactions(self):
        for asset in self.wallets:
            self._transaction_lists[asset] = filter(
                self._tx_filter,
                self._transaction_lists[asset]
            )

    def _tx_filter(self, tx):
        addresses = [entry for k, v in self.wallets.iteritems() for entry in v]
        if tx.data['source'] in self.wallets:
            return True
        if tx.data['destination'] in self.wallets:
            return True
        # TODO: Is this broken?
        if tx.data['destination'] == 'polo' and tx.data['source'] == 'polo':
            return True
        return False

    def make_asset_results(self):
        for asset in self._assets:
            self.results[asset] = {
                'FIFO': accounting.FIFO(self._transaction_lists[asset]),
                'LIFO': accounting.LIFO(self._transaction_lists[asset])
            }
