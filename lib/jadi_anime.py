import hashlib
import uuid
import json
import requests
import urllib
import base64
import re
import typing
import aiohttp
from io import BytesIO
from PIL import Image


class AnimeConverter:

    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        self.url = 'https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process'

    def is_base64(self, string: str) -> bool:
        """Check if the given string is a base64 encoded image

        :param string: String to check
        :return: True if the string is a base64 encoded image, False otherwise
        """
        pattern = re.compile(r'^([0-9a-zA-Z+/]{4})*(([0-9a-zA-Z+/]{2}==)|([0-9a-zA-Z+/]{3}=))?$')
        return len(string) % 4 == 0 and pattern.fullmatch(string) is not None

    def base64_encode(self, url: str) -> str:
        """Encode the image at the given url to base64

        :param url: image url or local path
        :return: base64 encoded image
        """
        if ';base64,' in url or self.is_base64(url):
            return url.split(';base64,')[1] if ';base64,' in url else url
        else:
            if 'http' in url:
                image = base64.b64encode(requests.get(url).content).decode()
            else:
                with open(url, 'rb') as f:
                    image = base64.b64encode(f.read()).decode()
            return image

    def convert(self, string: str) -> int:
        """Get the number of special characters in the given string

        :param string: string to check
        :return: the number of special characters in the given string
        """
        encoded_string = urllib.parse.quote(string)
        pattern = re.compile(r'%[89ABab]')
        return len(pattern.findall(encoded_string))

    def sign_v1(self, obj: dict) -> str:
        """Sign the given object using md5 algorithm

        :param obj: object to sign
        :return: the signed object
        """
        str_obj = json.dumps(obj)
        return hashlib.md5(
            ('https://h5.tu.qq.com' +
             str(len(str_obj) + (self.convert(str_obj))) +
             'HQ31X02e').encode()
        ).hexdigest()

    def to_anime(self, img: str, qqmode: str = 'global', proxy: typing.Union[str, None] = None) -> typing.Union[
        None, Image.Image, dict]:
        """Convert image to anime style

        :param img: image url or base64 or local path
        :param qqmode: qqmode, default is global | china
        :param proxy: proxy url, must be a string or None, like 'https://' or 'socks5://' default is None
        :return:
            - Image.Image if conversion is successful
            - dict with error code and message if error occurs
        :raises ValueError: if proxy is not a string or None, like 'https://' or 'socks5://'
        :raises FileNotFoundError: if image path is not found
        :raises requests.exceptions.RequestException: if the request failed
        """
        if qqmode.lower() not in ['global', 'china']:
            return {'code': -1, 'error': 'QQ Mode not Found, use GLOBAL or CHINA only'}

        if proxy and (proxy.startswith('https://') or proxy.startswith('socks5://')):
            pass
        elif proxy is None:
            pass
        else:
            raise ValueError('Proxy must be a string or None, like "https://" or "socks5://"')

        img_data = self.base64_encode(img)
        if not img_data:
            raise FileNotFoundError("Image not found")
        obj = {
            'busiId': 'ai_painting_anime_entry' if qqmode.lower() == 'china' else 'different_dimension_me_img_entry',
            'extra': json.dumps({
                'face_rects': [],
                'version': 2,
                'platform': 'web',
                'data_report': {
                    'parent_trace_id': str(uuid.uuid4()),
                    'root_channel': '',
                    'level': 0,
                }
            }),
            'images': [img_data],
        }
        try:
            response = requests.post(self.url, data=json.dumps(obj), headers={
                'Content-Type': 'application/json',
                'Origin': 'https://h5.tu.qq.com',
                'Referer': 'https://h5.tu.qq.com/',
                'User-Agent': self.user_agent,
                'x-sign-value': self.sign_v1(obj),
                'x-sign-version': 'v1',
            }, proxies={"https": proxy, "http": proxy} if proxy else None)
        except requests.exceptions.RequestException as e:
            raise e

        if response.status_code != 200:
            raise ValueError("Failed to convert image: " + response.text)

        data = json.loads(response.text)

        if data["code"] != 0:
            return data

        data = json.loads(data['extra'])

        resp = requests.get(data['img_urls'][0], headers={'User-Agent': self.user_agent})
        img = Image.open(BytesIO(resp.content))
        box = (img.width // 2 + 10, 30, img.width - 30, img.height - 205)
        return img.crop(box)

    async def async_to_anime(self, img: str, qqmode: str = 'global', proxy: typing.Union[str, None] = None) -> typing.Union[
    None, Image.Image, dict]:
        """Convert image to anime style

        :param img: image url or base64 or local path
        :param qqmode: qqmode, default is global | china
        :param proxy: proxy url, must be a string or None, like 'https://' or 'socks5://' default is None
        :return:
            - Image.Image if conversion is successful
            - dict with error code and message if error occurs
        :raises ValueError: if proxy is not a string or None, like 'https://' or 'socks5://'
        :raises FileNotFoundError: if image path is not found
        :raises requests.exceptions.RequestException: if the request failed
        """
        if qqmode.lower() not in ['global', 'china']:
            return {'code': -1, 'error': 'QQ Mode not Found, use GLOBAL or CHINA only'}

        if proxy and (proxy.startswith('https://') or proxy.startswith('socks5://')):
            pass
        elif proxy is None:
            pass
        else:
            raise ValueError('Proxy must be a string or None, like "https://" or "socks5://"')

        img_data = self.base64_encode(img)
        if not img_data:
            raise FileNotFoundError("Image not found")
        obj = {
            'busiId': 'ai_painting_anime_entry' if qqmode.lower() == 'china' else 'different_dimension_me_img_entry',
            'extra': json.dumps({
                'face_rects': [],
                'version': 2,
                'platform': 'web',
                'data_report': {
                    'parent_trace_id': str(uuid.uuid4()),
                    'root_channel': '',
                    'level': 0,
                }
            }),
            'images': [img_data],
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, data=json.dumps(obj), headers={
                    'Content-Type': 'application/json',
                    'Origin': 'https://h5.tu.qq.com',
                    'Referer': 'https://h5.tu.qq.com/',
                    'User-Agent': self.user_agent,
                    'x-sign-value': self.sign_v1(obj),
                    'x-sign-version': 'v1',
                }, proxy=proxy) as response:
                    if response.status != 200:
                        raise ValueError("Failed to convert image: " + await response.text())
                    data = json.loads(await response.text())
        except requests.exceptions.RequestException as e:
            raise e

        if data["code"] != 0:
            return data

        data = json.loads(data['extra'])

        async with aiohttp.ClientSession() as session:
            async with session.get(data['img_urls'][0], headers={'User-Agent': self.user_agent}) as resp:
                img = Image.open(BytesIO(await resp.read()))
                box = (img.width // 2 + 10, 30, img.width - 30, img.height - 205)
                return img.crop(box)