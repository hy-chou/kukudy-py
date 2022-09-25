from datetime import datetime, timezone
from json import dump
from os import makedirs


def append(path='', lines=''):
    makedirs(path[:path.rfind('/')], exist_ok=True)
    with open(path, 'a') as f:
        f.write(lines)


def appendjson(path='', data=[]):
    makedirs(path[:path.rfind('/')], exist_ok=True)
    with open(path, 'a') as f:
        dump(data, f, separators=(',', ':'))


def get_ts():
    return datetime.now(timezone.utc).isoformat()[:19].replace(':', '.')
