from . import dalle
from PIL import Image, ImageDraw, ImageFont


class Dalle:

    def __init__(self, prompt: str, author: str):
        self.prompt = prompt
        self.author = author

    def create_collage(self, query: str, source_image: Image, images: list) -> str:
        width = source_image.width
        height = source_image.height
        font_size = 30
        spacing = 16
        text_height = font_size + spacing
        new_im = Image.new('RGBA', (width * 3 + spacing * 2, height * 3 + spacing * 2 + text_height),
                           (0, 0, 0, 0))

        index = 0
        for i in range(0, 3):
            for j in range(0, 3):
                im = Image.open(images[index].path)
                im.thumbnail((width, height))
                new_im.paste(im, (i * (width + spacing), text_height + j * (height + spacing)))
                index += 1

        img_draw = ImageDraw.Draw(new_im)
        fnt = ImageFont.truetype("assets/fonts/FiraMono-Medium.ttf", font_size)
        img_draw.text((1, 0), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((0, 1), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((1, 2), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((2, 1), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((0, 0), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((0, 2), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((2, 0), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((2, 2), query, font=fnt, fill=(0, 0, 0))
        img_draw.text((1, 1), query, font=fnt, fill=(255, 255, 255))
        new_im.save(f"./generated/{self.author}/art.png")
        return f"generated/{self.author}/art.png"

    def generate(self) -> str:
        try:
            dall_e = dalle.DallE(self.prompt, self.author)
            images = dall_e.generate()

            if len(images) > 0:
                first_image = Image.open(images[0].path)
                return self.create_collage(self.prompt, first_image, images)
        except dalle.DallENoImagesReturned:
            print("DALL·E Mini API had no images for {query}.")
        except dalle.DallENotJson:
            print("DALL·E API Serialization Error, please try again later.")
        except dalle.DallEParsingFailed:
            print("DALL·E Parsing Error, please try again later.")
        except dalle.DallESiteUnavailable:
            print("DALL·E API Error, please try again later.")
        except Exception as e:
            print("Internal Error, please try again later.")
            print(repr(e))
