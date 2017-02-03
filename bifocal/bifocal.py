import models
import apis
import accounting
import utils


class Bifocal:

    def __init__(self, addresses={}, polo_key=None,
                 polo_secret=None, blocktrail_key=None):

        self.wallets = {}
        self._polo = apis.Polo(polo_key, polo_secret)
        self._blocktrail = apis.Blocktrail(blocktrail_key)
        self.results = {}
        for asset in addresses:
            self.wallets[asset] = models.Wallet(addresses[asset])
            self._make_transaction_lists(asset)
            self._add_polo_sales(asset)
            self._add_blacklists(asset)
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

    def _add_blacklists(self, asset):
        deps, withs = self._polo.get_deposits_and_withdrawals(asset)
        blacklist = [tx.data['id'] for tx in deps + withs]
        self.wallets[asset].add_blacklist_ids(blacklist)

    def _make_asset_results(self, asset):
        print self.wallets[asset].transactions
        fifo = accounting.FIFO(self.wallets[asset].transactions)
        print self.wallets[asset].transactions
        lifo = accounting.LIFO(self.wallets[asset].transactions)
        print self.wallets[asset].transactions
        self.results[asset] = {
            'FIFO': fifo,
            'LIFO': lifo}
