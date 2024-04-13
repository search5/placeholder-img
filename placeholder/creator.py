from collections import namedtuple
from io import BytesIO
import os
import sys
import importlib

from PIL import ImageFont, Image, ImageDraw, ImageColor
import importlib._bootstrap


def get_abs_filepath(package, path):
    spec = importlib.util.find_spec(package)
    mod = (sys.modules.get(package) or importlib._bootstrap._load(spec))
    parts = path.split("/")
    parts.insert(0, os.path.dirname(mod.__file__))
    return os.path.join(*parts)


FONT_PATH = get_abs_filepath('placeholder', 'public/NotoSansKR-Regular.ttf')


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