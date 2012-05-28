from datetime import datetime, timedelta

from zope.interface import Interface, Invalid
from zope.component import adapts
from zope.i18n import MessageFactory
from zope.datetime import parseDatetimetz
from zojax.widget.captcha.utils import decrypt, parseKey, encrypt1, getWord

from z3c.form.validator import SimpleFieldValidator

from interfaces import ICaptchaField, ICaptchaConfiglet
from zope.component._api import getUtility, getMultiAdapter
from zope.traversing.api import traverse
from zope.app.component.hooks import getSite
from zope.schema import ValidationError

_ = MessageFactory('zojax.widget.captcha')

class WrongCaptchaCode(ValidationError):
    __doc__ = _("""The code you entered was wrong, please enter the new one.""")


class CaptchaValidator(SimpleFieldValidator):
    """Captcha validator"""

    adapts(Interface, Interface, Interface, ICaptchaField, Interface)

    def validate(self, value):
        self.configlet = getUtility(ICaptchaConfiglet)

        if self.configlet.type == 'captcha':
            # Verify the user input against the captcha
            errors = ()
            context = self.context
            request = self.request
            value = value or ''
            captcha_type = self.configlet.captchaType
            if captcha_type in ['static', 'dynamic']:
                hashkey = request.get('%shashkey' % self.widget.form.prefix, '')
                decrypted_key = decrypt(self.configlet.captchaKey, hashkey)
                parsed_key = parseKey(decrypted_key)

                index = parsed_key['key']
                try:
                    date = parseDatetimetz(parsed_key['date'])
                except SyntaxError:
                    date = datetime.datetime(1000, 01, 01)

                if captcha_type == 'static':
                    solution = open(traverse(getSite(), '/@@/zojax-widget-captcha/captchas/%s.jpg.metadata' % index, request=request).chooseContext().path).read()
                    enc = encrypt1(value)
                else:
                    enc = value
                    solution = getWord(int(index))
                if (enc != solution) or (self.configlet.has_key(decrypted_key)) or (parseDatetimetz(str(datetime.now())) - date > timedelta(minutes=configlet.timeoutMins)):
                    raise ValueError(_(u'Please re-enter validation code.'))
                else:
                    self.configlet.addExpiredKey(decrypted_key)
        else:
            if not self.configlet.verify(self.request):
                raise WrongCaptchaCode
            else:
                return True