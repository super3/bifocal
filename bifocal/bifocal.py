import models
import apis
import accounting
import utils
import parsing


class Bifocal(object):

    def __init__(self, year=None, addresses={}, polo_key=None,
                 polo_secret=None, blocktrail_key=None, coinbase_csv=None):

        self.wallets = {}
        self.results = {}
        self.coinbase_csv = coinbase_csv

        if polo_secret is not None and polo_key is not None:
            self._polo = apis.Polo(polo_key, polo_secret)
        else:
            self._polo = None

        self._blocktrail = apis.Blocktrail(blocktrail_key)

        for asset in addresses:
            self.wallets[asset] = models.Wallet(addresses[asset])
            self._make_transaction_lists(asset)

            if self._polo is not None:
                self._add_polo_sales(asset)
                self._add_polo_blacklist(asset)
            if self.coinbase_csv is not None:
                self._add_coinbase_transactions()
                self._add_coinbase_blacklist()

            self.wallets[asset].finalize_tx_list()
            self._make_asset_results(asset)

    def _make_transaction_lists(self, asset):
        if asset == 'BTC':
            self.wallets[asset].add_transactions(utils.flatten(map(
                self._blocktrail.get_address_transactions,
                self.wallets[asset].addresses)))
        else:
            self.wallets[asset].add_transactions(utils.flatten(map(
                (lambda a: apis.Blockscan.get_address_transactions(a, asset)),
                self.wallets[asset].addresses)))

    def _add_polo_sales(self, asset):
        if asset != 'BTC':
            # assumes all non-btc assets are paired to BTC
            # each transaction is paired with a counter tx
            # I.e. every sale of SJCX is also a purchase of BTC
            txs, counter_txs = self._polo.get_trade_history(
                'BTC_' + asset)
            self.wallets[asset].add_transactions(txs)
            self.wallets['BTC'].add_transactions(counter_txs)

    def _add_polo_blacklist(self, asset):
        deps, withs = self._polo.get_deposits_and_withdrawals(asset)
        blacklist = [tx.data['id'] for tx in deps + withs]
        self.wallets[asset].add_blacklist_ids(blacklist)

    def _add_coinbase_blacklist(self):
        pass

    def _add_coinbase_transactions(self):
        pass

    def _make_asset_results(self, asset):
        fifo = accounting.FIFO(self.wallets[asset].transactions)
        lifo = accounting.LIFO(self.wallets[asset].transactions)
        self.results[asset] = {
            'FIFO': fifo,
            'LIFO': lifo}

    def print_balances(self):
        pass
