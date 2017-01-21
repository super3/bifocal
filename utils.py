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
    ret_json = json.loads(ret.text)
    return ret_json


def encode_args(self, args_dict):
    payload = ''
    for key, value in args_dics.iteritems():
        payload += "%s=%s&" % (key, value)
    return payload[:-1]
