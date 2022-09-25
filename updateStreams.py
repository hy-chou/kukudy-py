from math import ceil
from sys import argv

from dotenv import dotenv_values
from requests import get

from utils import append, appendjson, get_ts

config = dotenv_values("../.env")


def log_streams(ts, res, page_num):
    ts2H = ts[:13]

    rtt = res.elapsed.total_seconds()
    append(f'./rtts/uS/{ts2H}.tsv', f'{ts}\t{rtt}\n')

    for k, v in res.headers.items():
        append(f'./hdrs/{ts2H}/{k}.tsv', f'{ts}\t{v}\n')

    data = res.json()['data']
    appendjson(f'./raws/{ts2H}/{ts}p{page_num}.json', data)

    lines = ''
    for i in data:
        lines += i['user_login'] + '\t'
    append(f'./ulgs/p{page_num}/{ts2H}/{ts}.tsv', lines[:-1] + '\n')


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


def update_streams(page_to_do=1, page_num=1, cursor=''):
    ts = get_ts()
    res = get_streams(cursor)

    new_cursor = res.json()['pagination']['cursor']

    log_streams(ts, res, page_num)
    if page_to_do > 1:
        update_streams(page_to_do - 1, page_num + 1, new_cursor)


if __name__ == '__main__':
    if len(argv) != 2:
        update_streams(1)
    else:
        page_to_do = ceil(int(argv[1])/100)
        update_streams(page_to_do)
