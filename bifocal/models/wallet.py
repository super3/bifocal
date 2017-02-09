class Wallet(object):
    def __init__(self, addresses=None, transactions=None,
                 blacklist=None, exchanges=None):
        self.addresses = [] if addresses is None else addresses
        self.transactions = [] if transactions is None else transactions
        self.blacklist = [] if blacklist is None else blacklist
        self.exchanges = [] if exchanges is None else exchanges

    def finalize_tx_list(self):
        self.transactions = sorted(
            self.transactions,
            key=lambda k: k.timestamp)
        self.transactions = filter(self._tx_filter, self.transactions)
        self.transactions = map(self._check_transaction_sign,
                                self.transactions)

    def _tx_filter(self, tx):
        source, destination = tx.data['source'], tx.data['destination']
        wallet = self.addresses + self.exchanges

        if tx.data['id'] in self.blacklist:
            return False
        if tx.data['source'] in self.blacklist:
            return False
        if tx.data['destination'] in self.blacklist:
            return False
        if source in wallet and destination not in wallet:
            return True
        if destination in wallet and source not in wallet:
            return True
        if source in self.exchanges and destination in self.exchanges:
            return True
        return False

    def _check_transaction_sign(self, tx):
        source, destination = tx.data['source'], tx.data['destination']

        if source in self.addresses and tx.quantity > 0:
            tx.invert_quantity()
        if destination in self.addresses and tx.quantity < 0:
            tx.invert_quantity()

        return tx
