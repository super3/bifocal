import calendar
from datetime import datetime
import json
import math


def date_to_timestamp(date, form):
    """
    Parse a UTC timestamp from a datetime string
    """
    time = datetime.strptime(date, form)
    timestamp = calendar.timegm(time.utctimetuple())
    return timestamp


def timestamp_to_date(timestamp, form):
    """
    Return a date string from a timestamp
    """
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


def flatten(l):
    """
    Flatten a list of lists
    """
    return [i for s in l for i in s]


def distribute(inputs, outputs):
    """
    Builds a nested dictionary assigning inputs to outputs.
    """
    total_inputs = sum(inputs[key] for key in inputs)
    total_outputs = sum(outputs[key] for key in outputs)
    fee = total_inputs - total_outputs

    tx_map = {}

    for i, in_val in inputs.iteritems():
        txns = {}
        proportion = float(in_val) / total_inputs

        for o, out_val in outputs.iteritems():
            value = int(math.floor(out_val * proportion))
            txns[o] = value

        txns['fee'] = int(math.floor(fee * proportion))

        missing_value = in_val - sum(txns[k] for k in txns)
        for key, value in txns.iteritems():
            value += 1
            missing_value -= 1
            if missing_value == 0:
                break

        tx_map[i] = txns

    return tx_map
