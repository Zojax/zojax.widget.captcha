from datetime import datetime, timedelta

from zope.interface import Interface, Invalid
from zope.component import adapts
from zope.i18n import MessageFactory
from zope.datetime import parseDatetimetz
from zojax.widget.captcha.utils import decrypt, parseKey, encrypt1, getWord

from z3c.form.validator import SimpleFieldValidator

from interfaces import ICaptchaField, ICaptchaConfiglet
from zope.component._api import getUtility
from zope.traversing.api import traverse
from zope.app.component.hooks import getSite

_ = MessageFactory('zojax.widget.captcha')

class CaptchaValidator(SimpleFieldValidator):
    """Captcha validator"""

    adapts(Interface, Interface, Interface, ICaptchaField, Interface)

    def validate(self, value):
        # Verify the user input against the captcha
        errors = ()
        context = self.context
        request = self.request
        value = value or ''
        configlet = getUtility(ICaptchaConfiglet)
        captcha_type = configlet.type
        if captcha_type in ['static', 'dynamic']:
            hashkey = request.get('%shashkey' % self.widget.form.prefix, '')
            decrypted_key = decrypt(configlet.captchaKey, hashkey)
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
            if (enc != solution) or (configlet.has_key(decrypted_key)) or (parseDatetimetz(str(datetime.now())) - date > timedelta(minutes=configlet.timeoutMins)):
                raise ValueError(_(u'Please re-enter validation code.'))
            else:
                configlet.addExpiredKey(decrypted_key)
