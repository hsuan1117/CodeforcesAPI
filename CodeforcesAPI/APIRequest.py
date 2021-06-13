import json
import pathlib
from time import time
from urllib.parse import urlencode
from hashlib import sha512, md5


def call_api(parent, endpoint='contest.status', data=None, cache_file=None, cache_time=None):
    """
    :param cache_time: 快取時間
    :param cache_file: 指定cache file 例如： status.json
    :param data: 其他要傳送的data
    :param endpoint: API endpoint
    :param parent: 必須傳入self
    """
    f = None
    if parent.cache:  # 如果要cache
        pathlib.Path('cache/').mkdir(parents=True, exist_ok=True)
        if cache_file is not None:  # 如果有限定 cache file
            f = pathlib.Path(f'cache/{cache_file}.json')
        elif data is not None:  # 沒限定，自己生
            f = pathlib.Path(f'cache/{endpoint}-{md5(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()[:5]}.json')
        else:  # 什麼都沒限定,用endpoint
            f = pathlib.Path(f'cache/{endpoint}')

        if f.exists() and f.stat().st_size != 0 and int(time()) - int(
                f.stat().st_mtime) < (cache_time or 3 * 60):
            return json.load(f.open('r'))

    # cache 不適用
    default_data = {
        'apiKey': parent.apiKey,
        'time': int(time())
    }
    if data is None:
        data = {}

    # merge two dict
    final_data = {**data, **default_data}
    post_data = urlencode([(k,final_data[k]) for k in sorted(final_data.keys())])
    # print(post_data)
    api_sig = sha512(f'123456/{endpoint}?{post_data}#{parent.secret}'.encode()).hexdigest()
    res = parent.session.get(f'https://codeforces.com/api/{endpoint}?{post_data}',
                             params={'apiSig': '123456' + api_sig})

    api_json = json.loads(res.text)
    if api_json['status'] == 'FAILED':
        # print(api_json['comment'])
        from CodeforcesAPI.Exceptions import CodeforcesCredentialException
        raise CodeforcesCredentialException(message=api_json['comment'])

    if parent.cache:  # 如果要cache
        json.dump(api_json['result'], f.open('w+'))

    return api_json['result']
