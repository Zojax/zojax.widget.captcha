from zope.interface import implements
from zope.schema import ASCIILine
from zojax.widget.captcha.interfaces import ICaptchaField

class Captcha(ASCIILine):
    implements(ICaptchaField)
