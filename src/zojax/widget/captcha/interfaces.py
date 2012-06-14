from zope import interface, schema
from zope.i18n import MessageFactory
from zojax.widget.radio.field import RadioChoice

_ = MessageFactory('zojax.widget.captcha')


class ICaptchaConfiglet(interface.Interface):

    recaptchaPublicKey = schema.TextLine(title=_(u'Recaptcha Pulic Key'),
                                         default=u'6LfXutISAAAAANV5BL43MxP6JoRYJdmYv3_MU3N2',
                                         required=True)

    recaptchaPrivateKey = schema.TextLine(title=_(u'Recaptcha Private Key'),
                                          default=u'6LfXutISAAAAAAcNGkriCBGHjujZkU-GGMGxpkco',
                                          required=True)


class ICaptchaField(schema.interfaces.IASCIILine):
    u"""A field for captcha validation"""

