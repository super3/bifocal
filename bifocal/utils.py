import calendar
from datetime import datetime
import json


def date_to_timestamp(date, form):
    """
    Parse a UTC timestamp from a datetime string to a utc timestamp int
    """
    time = datetime.strptime(date, form)
    timestamp = calendar.timegm(time.utctimetuple())
    return timestamp


def timestamp_to_date(timestamp, form):
    date = datetime.utcfromtimestamp(timestamp)
    return date.strftime(form)


def timestamp_floor(timestamp):
    """
    Round a unix timestamp to the previous midnight
    """
    return timestamp / 86400 * 86400


def parse_json(ret):
    """
    Return a dictionary from a requests response
    """
    return json.loads(ret.text)


def encode_args(args_dict):
    """
    Encode a dictionary for url encoding. Example: 'key=val&key2=val2'
    """
    encoded = ''
    for key, value in args_dict.iteritems():
        encoded += "%s=%s&" % (key, value)
    return encoded[:-1]


def sort_by_timestamp(transactions):
    return sorted(transactions, key=lambda k: k.timestamp)


def flatten(l):
    return [i for s in l for i in s]
