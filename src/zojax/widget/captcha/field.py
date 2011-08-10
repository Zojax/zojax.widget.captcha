from zope.interface import implements
from zope.schema import ASCIILine
from zojax.widget.captcha.interfaces import ICaptcha

class Captcha(ASCIILine):
    implements(ICaptcha)
