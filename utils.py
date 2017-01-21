import calendar
import datetime
import json


def get_address_transactions(address, asset):
    pass


def datetime_to_timestamp(date, format):
    """
    Parse a UTC timestamp from a datetime string to a utc timestamp int
    """
    time = datetime.strptime(date, format)
    timestamp = calendar.timegm(time.utctimetuple())
    return timestamp


def timestamp_floor(timestamp):
    """
    Round a unix timestamp to the previous midnight
    """
    return timestamp / 86400 * 86400


def parse_json(self, ret):
    """
    Return a dictionary from a requests response
    """
    ret_json = json.loads(ret.text)
    return ret_json


def encode_args(self, args_dict):
    """
    Encode a dictionary for url encoding. Example: 'key=val&key2=val2'
    """
    encoded = ''
    for key, value in args_dics.iteritems():
        encoded += "%s=%s&" % (key, value)
    return encoded[:-1]


def sort_by_timestamp(transactions):
    return sorted(transactions, key=lambda k: k.timestamp)
