class Wallet:
    def __init__(self, addresses, transactions=[], blacklist=[]):
        self._addresses = addresses
        self.transactions = transactions
        self.blacklist = blacklist

    def add_addresses(self, new):
        self._addresses += set(new) - set(self._addresses)

    def add_transactions(self, new):
        self.transactions = set(new) - set(self.transactions)

    def add_blacklist_ids(self, new):
        self.blacklist = set(new) - set(self.blacklist)

    def check_tx_list(self):
        self._sort_transactions()
        self._filter_transactions()
        self._check_transaction_signs()

    def _sort_transactions(self):
        self.transactions = sorted(
            self.transactions,
            key=lambda k: k.timestamp)

    def _filter_transactions(self):
        self._addresses = filter(
            self._tx_filter,
            self.transactions)

    def _tx_filter(self, tx):
        source, destination = tx.data['source'], tx.data['destination']
        if tx.data['id'] in self.blacklist:
            return False
        if source in self._addresses and destination not in self._addresses:
            return True
        if destination in self._addresses and source not in self._addresses:
            return True
        if souce == 'polo' and destination == 'polo':
            return True
        return False

    def _check_transaction_signs(self):
        for tx in self.transactions:
            source, destination = tx.data['source'], tx.data['destination']

            if source == 'polo' and destination == 'polo':
                continue

            if source in self._addresses and tx.quantity > 0:
                tx.invert_quantity()
            if destination in self._addresses and tx.quantity < 0:
                tx.invert_quantity()
