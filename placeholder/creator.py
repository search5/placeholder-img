from collections import namedtuple
from io import BytesIO
import os
import importlib.resources as pkg_resources

from PIL import ImageFont, Image, ImageDraw, ImageColor


FONT_PATH = pkg_resources.files('placeholder.public').joinpath('NotoSansKR-Regular.ttf')
print(FONT_PATH)


def _parse_size(size):
    Size = namedtuple('Size', ['width', 'height'])
    try:
        width, height = size.split('x')
    except ValueError:
        width = height = size

    try:
        size = Size(int(width), int(height))
    except ValueError:
        size = Size(1, 1)

    return size


def _parse_colors(bgcolor, color):
    try:
        bgcolor = ImageColor.getrgb(bgcolor)
    except ValueError:
        try:
            bgcolor = ImageColor.getrgb('#%s' % bgcolor)
        except ValueError:
            bgcolor = ImageColor.getrgb('#DDD')

    try:
        color = ImageColor.getrgb(color)
    except ValueError:
        try:
            color = ImageColor.getrgb('#%s' % color)
        except ValueError:
            color = ImageColor.getrgb('#888')
    return bgcolor, color


def makeplaceholder(size, text=None, bgcolor="FFF", color="888", format='PNG', font_size=None):
    size = _parse_size(size)
    bgcolor, color = _parse_colors(bgcolor, color)
    image = Image.new('RGB', size, bgcolor)
    draw = ImageDraw.Draw(image)
    text = text if text else "%s x %s" % size
    calculated_font_size = ((size.width - 10) / len(text)) * 2
    font_size = font_size if font_size else calculated_font_size
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        font = ImageFont.load_default()
    text_size = draw.textbbox((0, 0), text, font=font)[2:]
    text_center = (size.width / 2 - text_size[0] / 2,
                    size.height / 2 - text_size[1] / 2)
    draw.text(text_center, text, fill=color, font=font)
    fp = BytesIO()
    image.save(fp, format)

    return fp.getvalue()
