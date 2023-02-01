# You can find original code here: https://github.com/rawandahmad698/Dalle-Discord
# This code is remade for support sync request

from pathlib import Path

import base64
import requests


# ** Exceptions **

class DallESiteUnavailable(Exception):
    """
    Raised when the DallE API is unavailable.
    """
    pass


# DallE Parsing failed
class DallEParsingFailed(Exception):
    """
    Raised when the DallE API returns an error.
    """
    pass


class DallENotJson(Exception):
    """
    Raised when the DallE API returns an error.
    """
    pass


class DallENoImagesReturned(Exception):
    """
    Raised when the DallE API returns no images.
    """
    pass


# ** Exceptions End **


class GeneratedImage:
    def __init__(self, image_name: str, image_path: str):
        self.image_name = image_name
        self.path = image_path


class DallE:
    def __init__(self, prompt: str, author: str):
        self.prompt = prompt
        self.author = author

    def generate(self) -> list[GeneratedImage]:
        """
        Makes an api request to dall-e endpoint and returns the images
        :return: list
        """
        url = "https://bf.dallemini.ai/generate"

        payload = {
            "prompt": self.prompt
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://hf.space',
            'Referer': 'https://hf.space/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/15.5 Safari/605.1.15 '
        }

        # Make a request with requests
        r = requests.post(url, json=payload, headers=headers)
        if r.status_code == 200:
            if r.headers['Content-Type'] == 'application/json':
                res = r.json()
                images = res['images']
                generated_images = []

                if len(images) == 0:
                    raise DallENoImagesReturned()

                v = 0
                for image in images:
                    v += 1
                    converted = self.base_64_to_image(image, v)
                    generated_images.append(converted)

                return generated_images
            else:
                raise DallENotJson()
        else:
            raise DallESiteUnavailable()

    def base_64_to_image(self, base_64_string: str, number: int) -> GeneratedImage:
        """
        Converts a base64 string to an image
        :param number:
        :param base_64_string:
        :return: GeneratedImage
        """
        path = f"generated_{self.author}_{number}"

        Path(f"./generated/{self.author}").mkdir(parents=True,
                                                 exist_ok=True)  # Create the directory if it doesn't exist

        with open(f"./generated/{self.author}/{path}.jpg", "wb") as fh:
            fh.write(base64.urlsafe_b64decode(base_64_string))

        return GeneratedImage(path + ".jpg", f"./generated/{self.author}/{path}.jpg")


def test():
    dall_e = DallE(prompt="flower", author="DallE")
    generated = dall_e.generate()
    for image in generated:
        print(image.image_name)
        print(image.path)


if __name__ == '__main__':
    test()
