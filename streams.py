from datetime import datetime, timezone
from os import makedirs
from telnetlib import TLS

from dotenv import dotenv_values
from requests import get

config = dotenv_values("../.env")


def get_streams(after='', first=100):
    url = 'https://api.twitch.tv/helix/streams'
    payload = {
        'first': first,
        'after': after,
    }
    headers = {
        'Authorization': 'Bearer ' + config['ACCESS_TOKEN'],
        'Client-Id': config['CLIENT_ID'],
    }

    return get(url, params=payload, headers=headers)


def parse_streams(res):
    rjson = res.json()
    data = rjson['data']
    cursor = rjson['pagination']['cursor']
    return data, cursor


def log_elapsed(res, ts):
    rtt = res.elapsed.total_seconds()
    pdir = f'./{ts[:13]}'
    makedirs(pdir, exist_ok=True)
    with open(f'{pdir}/elapses.txt', 'a') as f:
        f.write(f'{ts}\t{rtt}\n')


def log_headers(res, ts):
    pdir = f'./{ts[:13]}/headers'
    makedirs(pdir, exist_ok=True)
    for key in res.headers:
        with open(f'{pdir}/{key}.txt', 'a') as f:
            if key == 'Ratelimit-Reset':
                rreset = int(res.headers[key])
                rreset = datetime.fromtimestamp(rreset).isoformat()
                f.write(f'{ts}\t{rreset}\n')
            else:
                f.write(f'{ts}\t{res.headers[key]}\n')


def log_streams(streams, ts, pagenum):
    pdir = f'./{ts[:13]}/streams/p{pagenum}'
    makedirs(pdir, exist_ok=True)
    with open(f'{pdir}/{ts[:19]}.txt', 'a') as f:
        for stream in streams:
            f.write('\t'.join([str(i) for i in stream.values()]) + '\n')


if __name__ == '__main__':
    cursor = ''
    for i in range(10):
        ts = datetime.now(timezone.utc).isoformat()[:19].replace(':', '.')
        res = get_streams(cursor)
        data, cursor = parse_streams(res)
        log_elapsed(res, ts)
        log_headers(res, ts)
        log_streams(data, ts, i)
