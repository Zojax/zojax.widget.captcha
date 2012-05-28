from zope import interface, schema
from zope.i18n import MessageFactory
from zojax.widget.radio.field import RadioChoice

_ = MessageFactory('zojax.widget.captcha')


class ICaptchaConfiglet(interface.Interface):

    timeoutMins = schema.Int(title=_(u'Timeout minutes'),
                             default=60,
                             required=False)
    
    limit = schema.Int(title=_(u'Limit'),
                             default=0,
                             required=False)

    periodSeconds = schema.Int(title=_(u'Period seconds'),
                             default=60,
                             required=False)
    
    captchaKey = schema.TextLine(title=_(u'Captcha key'),
                                  default=u'captcha_key',
                                  required=False)
    
    captchaType = RadioChoice(title=_(u'Captcha type'),
                       values=['static', 'dynamic'],
                       default='dynamic',
                       required=False)

    type = RadioChoice(title=_(u'Checking Type'),
                values=['captcha', 'recaptcha'],
                default='captcha')
    
    length = schema.Int(title=_(u'Captcha text length'),
                             default=7, min=3, required=False)
    
    letters = schema.Bool(title=_(u'Use letters'),
                                  default=True,
                                  required=False)
    
    digits = schema.Bool(title=_(u'Use digits'),
                                  default=True, required=False)
    
    imageSize = schema.Int(title=_(u"Image size"),
                           default=27)
    
    background = schema.TextLine(title=_(u'Background color'),
                                 default=u'grey', required=False)

    fontColor = schema.TextLine(title=_(u'Font color'),
                                 default=u'black', required=False)
    
    period = schema.Float(title=_(u"Period"),
                           default=0.1, required=False)

    amplitude = schema.Float(title=_(u"Amplitude"),
                           default=5., required=False)

    noise = schema.Int(title=_(u"Noise level"),
                           default=5, min=0, max=100, required=False)
    
    randomParams = schema.Bool(title=_(u'Random params'),
                                  default=True, required=False)

    recaptchaPublicKey = schema.TextLine(title=_(u'Recaptcha Pulic Key'), required=False)

    recaptchaPrivateKey = schema.TextLine(title=_(u'Recaptcha Private Key'), required=False)

    records = interface.Attribute('Records')
    
    def has_key(key):
        """has such key"""
        
    def addExpiredKey(key):
        """add expired key"""


class ICaptchaField(schema.interfaces.IASCIILine):
    u"""A field for captcha validation"""

