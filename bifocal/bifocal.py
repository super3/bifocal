import models
import apis
import accounting
import utils

# TODO: Get Polo deposit/withdrawals.
# Crawl transactions and filter out those ones by txid
# TODO: Check TX quantity signs


class Bifocal:

    def __init__(self, addresses={}, polo_key=None, polo_secret=None):

        self.wallets = {}
        self._polo = apis.Polo(polo_key, polo_secret)
        self.results = {}

        for asset in self.wallets:
            self.wallets[asset] = models.Wallet(addresses[asset])

        self.make_transaction_lists()
        self.make_asset_results()

    def make_transaction_lists(self):
        for asset in self.wallets:
            if asset != 'BTC':
                self._transaction_lists[asset] += utils.flatten(map(
                    (lambda a:
                     Blockscan.get_address_transactions(a, asset)),
                    self.wallets[asset]
                ))
        self._transaction_lists['BTC'] += utils.flatten(map(
            lambda a: Blocktail.get_address_transactions(a),
            self.wallets[asset]
        ))

        self._add_polo_sales()
        self._add_blacklists()

        for asset in self.wallets:
            self.wallets[asset].check_tx_list()

    def _add_polo_sales(self):
        for asset in self.wallets:
            if asset != 'BTC':
                # assumes all non-btc assets are paired to BTC
                # each transaction is paired with a counter tx
                # I.e. every sale of SJCX is also a purchase of BTC
                txs, counter_txs = self._polo.get_trade_history(
                    'BTC_' + asset)
                self.wallets[asset].add_transactions(txs)
                self.wallets['BTC'].add_transactions(counter_txs)

    def _add_blacklists(self):
        for asset in self.wallets:
            dep, withs = self._polo.get_deposits_and_withdrawls(asset)
            blacklist = [tx.data['id'] for tx in deps + withs]
            self.wallets.add_blacklist_ids(blacklist)

    def make_asset_results(self):
        for asset in self._assets:
            self.results[asset] = {
                'FIFO': accounting.FIFO(self._transaction_lists[asset]),
                'LIFO': accounting.LIFO(self._transaction_lists[asset])
            }
