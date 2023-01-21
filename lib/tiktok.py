from requests import Session
from typing import Union


class TikTok(Session):
    BASE_URL = 'https://www.tikwm.com'

    def __init__(self) -> None:
        super().__init__()

    def download(self, url: str) -> Union[dict, bytes]:
        try:
            r = self.post(f'{self.BASE_URL}/api/', data=dict(url=url, count=12, cursor=0, web=1, hd=1))
            res = r.json()
            if res['code'] == 0:
                return res['data']
            else:
                return {'code': res['code'], 'error': res['msg']}
        except Exception as e:
            print(e)
            return {'code': -1, 'error': 'Failed to download video'}
