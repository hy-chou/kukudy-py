from json import dump
from math import ceil
from os import makedirs
from sys import argv

from dotenv import dotenv_values
from requests import get

from kukudy.utils import get_ts

config = dotenv_values("../.env")


def get_streams(cursor='', num=100):
    url = 'https://api.twitch.tv/helix/streams'
    payload = {
        'first': num,
        'after': cursor,
    }
    headers = {
        'Authorization': 'Bearer ' + config['ACCESS_TOKEN'],
        'Client-Id': config['CLIENT_ID'],
    }

    return get(url, params=payload, headers=headers)


def parse_response(res):
    rtt = res.elapsed.total_seconds()
    headers = res.headers
    data = res.json()['data']
    cursor = res.json()['pagination']['cursor']

    return rtt, headers, data, cursor


def log_streams(ts, rtt, headers, data):
    ts2H = ts[:13]
    makedirs(f'./{ts2H}/data', exist_ok=True)

    with open(f'./{ts2H}/rtt.txt', 'a') as f:
        f.write(f'{ts}\t{rtt}\n')

    for k, v in headers.items():
        with open(f'./{ts2H}/{k}.txt', 'a') as f:
            f.write(f'{ts}\t{v}\n')

    with open(f'./{ts2H}/data/{ts}.json', 'a') as f:
        dump(data, f, separators=(',', ':'))


def update_streams(num_page):
    cursor = ''

    for _ in range(num_page):
        ts = get_ts()
        res = get_streams(cursor)
        rtt, headers, data, cursor = parse_response(res)

        log_streams(ts, rtt, headers, data)


if __name__ == '__main__':
    num_page = ceil(int(argv[1])/100)
    if num_page > 0:
        update_streams(num_page)
