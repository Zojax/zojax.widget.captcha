import os
import re
import math
try:
    import hashlib as md5
    md5.md5
except ImportError:
    import md5
from string import atoi
from random import randint

from DateTime import DateTime

from zojax.widget.captcha.data import basic_english
#import zojax.widget.captcha configuration values
from zojax.widget.captcha.config import (DEFAULT_IMAGE_SIZE, DEFAULT_BG,
    DEFAULT_FONT_COLOR, DEFAULT_DISTORTION, CAPTCHAS_COUNT)

try:
    import Crypto.Cipher.DES as Crypto
    Crypto
except ImportError:
    import Crypto


def encrypt1(s):
    return md5.md5(s).hexdigest().upper()


def getTransform(x, y, a, p, o):
    return (math.sin((y + o[0]) * p) * a + x, math.sin((x + o[1]) * p) * a + y)


def gen_captcha(**kwargs):
    """Generate a captcha image"""
    try:
        from App import ImageFile
        ImageFile
    except ImportError:
        import ImageFile
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
    import random
    from PIL import ImageFile as pyImageFile
    import sys
    sys.modules['ImageFile'] = pyImageFile
    from cStringIO import StringIO

    text = kwargs.get('text', None)
    fnt_sz = kwargs.get('size', DEFAULT_IMAGE_SIZE)
    bkground = kwargs.get('bkground', DEFAULT_BG)
    font_color = kwargs.get('font_color', DEFAULT_FONT_COLOR)
    distortion = kwargs.get('distortion', DEFAULT_DISTORTION)

    period = distortion[0]
    amplitude = distortion[1]
    offset = distortion[2]

    outFile = StringIO()

    DATA_PATH = os.path.abspath(os.path.dirname(__file__)) + '/data'
    FONT_PATH = DATA_PATH + '/fonts'

    #select font for captcha text
    ALL_FONTS = ('Bd', 'It', 'MoBI', 'Mono', 'Se',
                 'BI', 'MoBd', 'MoIt', 'SeBd', '')
    rand_font = random.choice(ALL_FONTS)
    rand_font_path = FONT_PATH + '/vera/Vera%s.ttf' % rand_font
    font = ImageFont.truetype(rand_font_path, fnt_sz)
    textSize = font.getsize(text)

#------------------------------render   background1 -----------------------
    image = Image.new('RGB', (textSize[0] + 7, textSize[1] + 7), bkground)
    image.paste(bkground)
#------------------------------render       Text2 ------------------------
    draw = ImageDraw.Draw(image)
    alignment = (random.uniform(0, 1), random.uniform(0, 1))
    x = int((image.size[0] - textSize[0]) * alignment[0] + 0.5)
    y = int((image.size[1] - textSize[1]) * alignment[1] + 0.5)

    draw.text((x, y), text, font=font, fill=font_color)

#------------------------------render       Distortion -----------------------
    r = 1
    xPoints = image.size[0] / r + 2
    yPoints = image.size[1] / r + 2

    # Create a list of arrays with transformed points
    xRows = []
    yRows = []
    for j in xrange(yPoints):
        xRow = []
        yRow = []
        for i in xrange(xPoints):
            x, y = getTransform(i * r, j * r, amplitude, period, offset)

            # Clamp the edges so we don't get black undefined areas
            x = max(0, min(image.size[0] - 1, x))
            y = max(0, min(image.size[1] - 1, y))

            xRow.append(x)
            yRow.append(y)
        xRows.append(xRow)
        yRows.append(yRow)

    # Create the mesh list, with a transformation for
    # each square between points on the grid
    mesh = []
    for j in xrange(yPoints - 1):
        for i in xrange(xPoints - 1):
            mesh.append((
                # Destination rectangle
                (i * r, j * r,
                 (i + 1) * r, (j + 1) * r),
                # Source quadrilateral
                (xRows[j][i], yRows[j][i],
                 xRows[j + 1][i], yRows[j + 1][i],
                 xRows[j + 1][i + 1], yRows[j + 1][i + 1],
                 xRows[j][i + 1], yRows[j][i + 1]),
                ))

    img = image.transform(image.size, Image.MESH, mesh, Image.BILINEAR)

    # save the image to a file
    img.save(outFile, format='jpeg')
    outFile.seek(0)
    src = outFile.read()
    size = len(src)
    sys.modules['ImageFile'] = ImageFile
    return {'src': src, 'size': size}


def getWord(index):
    words = basic_english.words.split()
    return words[index]


def getIndex(word):
    words = basic_english.words.split()
    try:
        res = words.index(word)
    except ValueError:
        res = len(words) + 1
    return res


def getCaptchasCount(dynamic):
    if dynamic:
        return len(basic_english.words.split())
    else:
        return CAPTCHAS_COUNT


def formKey(num):
    def normalize(s):
        return (not len(s) % 8 and s) or normalize(s + str(randint(0, 9)))

    return normalize('%s_%i_' % (str(DateTime().timeTime()), num))


def encrypt(key, s):
    return toHex(Crypto.new(key).encrypt(s))


def decrypt(key, s):
    return Crypto.new(key).decrypt(toStr(s))


def parseKey(s):
    ps = re.match('^(.+?)_(.+?)_', s)
    if ps is None:
        return {'date': '', 'key': ''}
    return {'date': ps.group(1), 'key': ps.group(2)}


def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0' + hv
        lst.append(hv)

    return reduce(lambda x, y: x + y, lst)


def toStr(s):
    return s and chr(atoi(s[:2], base=16)) + toStr(s[2:]) or ''
