import models
import apis
import accounting
import utils
import parsing


# TODO: design this better and reimplement

class Bifocal(object):

    def __init__(self, year=None, addresses=None, polo_key=None,
                 polo_secret=None, blocktrail_key=None, coinbase_csv=None,
                 celery_csv=None):

        self.wallets = {}

        if addresses is not None:
            for asset in addresses:
                self.wallets[asset] = models.Wallet(addresses=addresses[asset])

        self.results = {}

        self._coinbase_csv = coinbase_csv
        self._celery_csv = celery_csv

        if polo_secret is not None and polo_key is not None:
            self._polo = apis.Polo(polo_key, polo_secret)
        else:
            self._polo = None

        if blocktrail_key is None:
            raise ValueError('Blocktrail Key Required')
        self._blocktrail = apis.Blocktrail(blocktrail_key)

        for asset in addresses:
            self._make_transaction_lists(asset)
            self._make_blacklists(asset)
            self.wallets[asset].finalize_tx_list()
            self._make_asset_results(asset)

    def _make_transaction_lists(self, asset):
        if asset == 'BTC':
            self.wallets['BTC'].transactions += utils.flatten(map(
                self._blocktrail.get_address_transactions,
                self.wallets['BTC'].addresses))

            if self._coinbase_csv is not None:
                self.wallets['BTC'].exchanges += ['Coinbase']
                self._add_coinbase_transactions()
            if self._celery_csv is not None:
                self.wallets['BTC'].exchanges += ['Celery']
                self._add_celery_transactions()

        else:
            self.wallets[asset].transactions += utils.flatten(map(
                (lambda a: apis.Blockscan.get_address_transactions(a, asset)),
                self.wallets[asset].addresses))
            if self._polo is not None:
                self._add_polo_sales(asset)

    def _make_blacklists(self, asset):
        if asset == 'BTC':
            if self._coinbase_csv is not None:
                self._add_coinbase_blacklist()
            if self._celery_csv is not None:
                self._add_celery_blacklist()

        if self._polo is not None:
            self._add_polo_blacklist(asset)

    def _add_polo_sales(self, asset):
        if asset != 'BTC':
            # assumes all non-btc assets are paired to BTC
            # each transaction is paired with a counter tx
            # I.e. every sale of SJCX is also a purchase of BTC
            txns, counter_txns = self._polo.get_trade_history(
                'BTC_' + asset)
            self.wallets[asset].exchanges += ['polo']

            self.wallets[asset].transactions += txns

        # TODO: this is broken.
        if asset == 'BTC':
            txns, counter_txns = self._polo.get_trade_history(
                'BTC_' + asset)
            self.wallets['BTC'].transactions += counter_txns

    def _add_polo_blacklist(self, asset):
        if asset != 'BTC':
            deps, withs = self._polo.get_deposits_and_withdrawals(asset)
            blacklist = [tx.data['source'] for tx in deps]
            blacklist += [tx.data['id'] for tx in withs]
            self.wallets[asset].blacklist += blacklist

        if assett == 'BTC':
            btc_blacklist = [tx.data['id'] for tx in withs]
            btc_blacklist += [tx.data['source'] for tx in deps]
            self.wallets['BTC'].blacklist += btc_blacklist

    def _add_coinbase_blacklist(self):
        blacklist = parsing.Coinbase.get_transfer_txids(self._coinbase_csv)
        self.wallets['BTC'].blacklist += blacklist

    def _add_coinbase_transactions(self):
        txns = parsing.Coinbase.get_transactions(self._coinbase_csv)
        self.wallets['BTC'].transactions += txns

    def _make_asset_results(self, asset):
        fifo = accounting.FIFO(self.wallets[asset].transactions)
        lifo = accounting.LIFO(self.wallets[asset].transactions)
        self.results[asset] = {
            'FIFO': fifo,
            'LIFO': lifo}

    def _add_celery_blacklist(self):
        blacklist = parsing.Celery.get_transfer_txids(self._celery_csv)
        self.wallets['BTC'].blacklist += blacklist

    def _add_celery_transactions(self):
        txns = parsing.Celery.get_transactions(self._celery_csv)
        self.wallets['BTC'].transactions += txns

    def print_balances(self):
        raise NotImplementedError
