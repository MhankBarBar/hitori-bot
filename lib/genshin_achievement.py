import typing
from PIL import Image, ImageDraw, ImageFont


def genshin_achievement(text: str) -> typing.Union[None, Image.Image]:
    """
    Generate an achievement image with a given text.

    Parameters
    ----------
    text : str
        The text to be displayed on the achievement image.

    Returns
    -------
    Union[None, Image.Image]
        An Image object representing the generated achievement image.
        None if the input text is empty.

    Examples
    --------
    >>> from genshin_achievement import genshin_achievement
    >>> img = genshin_achievement("Unlock Secret Achievement")
    >>> img.show()

    Notes
    -----
    The text will be trimmed to a maximum of 50 characters and added to the image.
    The image will be generated using the PIL library.
    """
    # Load font
    font_path = 'assets/fonts/zh-cn.ttf'
    font = ImageFont.truetype(font_path, size=28)

    # Load image
    img_path = 'assets/images/row-2-column-1.png'
    canvas = Image.open(img_path)
    ctx = ImageDraw.Draw(canvas)

    # Trim text and add quotes
    s = text.strip()
    if not s:
        return None
    if len(s) > 50:
        s = s[:50]
    space = (f'"{s}"'[:25]).rfind(' ')
    lines = [
        f'"{s[:space if space != -1 else 24] + ("" if space != -1 else "-")}',
        f'{s[space if space != -1 else 24:]}' + '"'
    ]

    # Split text into two lines if necessary
    if len(s) > 25:
        ctx.text((220, 125), lines[0], fill='#8c7d6f', font=font)
        ctx.text((225, 160), lines[1], fill='#8c7d6f', font=font)
    else:
        ctx.text((225, 140), f'"{s}"', fill='#8c7d6f', font=font)
    return canvas
