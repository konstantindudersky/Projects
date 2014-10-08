# coding=utf-8
"""
Добавляет в проект поддержку русских языков
"""

from reportlab.platypus import Image
from reportlab import rl_config
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import utils
from reportlab.lib.units import cm

FONT_FOLDER = "/usr/share/fonts/truetype/"


def add_russian_fonts():
    """
    Добавляет шрифты True type
    """
    # FreeFont
    rl_config.TTFSearchPath = FONT_FOLDER
    registerFont(TTFont('FreeSans', '/usr/share/fonts/truetype/FreeSans.ttf'))

    # Deja Vu
    rl_config.TTFSearchPath = FONT_FOLDER
    registerFont(TTFont('DejaVu Sans', FONT_FOLDER + 'DejaVuSans.ttf'))
    registerFont(TTFont('DejaVu Sans Bold', FONT_FOLDER + 'DejaVuSans-Bold.ttf'))
    registerFont(TTFont('DejaVu Sans Mono', FONT_FOLDER + 'DejaVuSansMono.ttf'))
    registerFont(TTFont('DejaVu Sans Mono Bold', FONT_FOLDER + 'DejaVuSansMono-Bold.ttf'))
    registerFont(TTFont('DejaVu Serif', FONT_FOLDER + 'DejaVuSerif.ttf'))
    registerFont(TTFont('DejaVu Serif Bold', FONT_FOLDER + 'DejaVuSerif-Bold.ttf'))

    # Droid
    rl_config.TTFSearchPath = FONT_FOLDER
    registerFont(TTFont('Droid Sans', FONT_FOLDER + 'DroidSans.ttf'))
    registerFont(TTFont('Droid Serif', FONT_FOLDER + 'DroidSerif-Regular.ttf'))


def get_image(path, width=1 * cm):
    """
    Загружает изображение и пропорционально масштабирует высоту и ширину
    :param path: Путь к изображению
    :param width: Ширина для отображения
    :return: Ссылку на изображение
    """
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


if __name__ == '__main__':
    add_russian_fonts()
