import models
import apis
import accounting
import utils


class Bifocal():

    def __init__(self, addresses=[], assets=[],
                 polo_key=None, polo_secret=None):

        self._polo = apis.Polo(polo_key, polo_secret)
        self._blockscan = apis.Blockscan()
        self._coindesk = apis.Coindesk()
        self._blockchain = apis.Blockchain()

        self._assets = assets
        self._transaction_lists = {}
        for asset in asset:
            self._transaction_lists['asset'] = []

        self._addresses = addresses
        self._add_exchange_addresses()

        self.wallet = models.Wallet(self._addresses)

        self.make_transaction_lists()

    def _add_exchange_addresses(self):
        self._add_polo_addresses()

    def _add_polo_addresses(self):
        for asset in self._assets:
            self._add_addresses(polo.get_deposit_addresses_by_asset(asset))

    def _add_addresses(self, addresses):
        self._addresses += set(addresses) - set(self._addresses)

    def _add_exchange_sales(self):
        self._add_polo_sales()

    def _add_polo_sales(self):
        for asset in self._assets:
            if asset != 'BTC':
                # assumes all non-btc assets are paired to BTC
                txs, counter_txs = self._polo.get_trade_history("BTC_" + asset)
                self._transaction_lists[asset] += txs
                self._transaction_lists['BTC'] += counter_txs

    def make_transaction_lists(self):
        for asset in self._assets:
            if asset != 'BTC':
                self._transaction_lists[asset] += map(
                    (lambda a:
                     self._blockscan.get_address_transactions(a, asset)),
                    self.wallet
                )
        self._transaction_lists['BTC'] += utils.flatten(map(
            lambda a: self._blockchain.get_address_transactions(a)
        ))
        self._add_exchange_sales()
        self._filter_transactions()
        self._sort_transactions()

    def _sort_transactions(self):
        for asset in assets:
            pass

    def _sort_tx_list(self):
        pass

    def _filter_transactions(self):
        for asset in assets:
            pass

    def _filter_tx_list(self, list):
        pass
