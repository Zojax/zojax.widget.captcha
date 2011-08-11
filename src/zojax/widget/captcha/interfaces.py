from zope import interface, schema
from zope.i18n import MessageFactory
from zojax.widget.radio.field import RadioChoice

_ = MessageFactory('zojax.widget.captcha')


class ICaptchaConfiglet(interface.Interface):

    timeoutMins = schema.Int(title=_(u'Timeout minutes'),
                             default=60)
    
    limit = schema.Int(title=_(u'Limit'),
                             default=0)

    periodSeconds = schema.Int(title=_(u'Period seconds'),
                             default=60)
    
    captchaKey = schema.TextLine(title=_(u'Captcha key'),
                                  default=u'captcha_key')
    
    type = RadioChoice(title=_(u'Captcha type'),
                       values=['static', 'dynamic'],
                       default='dynamic')
    
    imageSize = schema.Int(title=_(u"Image size"),
                           default=27)
    
    background = schema.TextLine(title=_(u'Background color'),
                                 default=u'grey')

    fontColor = schema.TextLine(title=_(u'Font color'),
                                 default=u'black')
    
    period = schema.Float(title=_(u"Period"),
                           default=0.1)

    amplitude = schema.Float(title=_(u"Amplitude"),
                           default=5.)
    
    randomParams = schema.Bool(title=_(u'Random params'),
                                  default=True)
    
    records = interface.Attribute('Records')
    
    def has_key(key):
        """has such key"""
        
    def addExpiredKey(key):
        """add expired key"""


class ICaptchaField(schema.interfaces.IASCIILine):
    u"""A field for captcha validation"""

