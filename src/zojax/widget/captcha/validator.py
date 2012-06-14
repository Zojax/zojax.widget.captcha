from datetime import datetime, timedelta

from zope.interface import Interface, Invalid
from zope.component import adapts
from zope.i18n import MessageFactory
from zope.datetime import parseDatetimetz

from z3c.form.validator import SimpleFieldValidator

from interfaces import ICaptchaField, ICaptchaConfiglet
from zope.component._api import getUtility, getMultiAdapter
from zope.traversing.api import traverse
from zope.app.component.hooks import getSite
from zope.schema import ValidationError
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE


_ = MessageFactory('zojax.widget.captcha')

class WrongCaptchaCode(ValidationError):
    __doc__ = _("""The code you entered was wrong, please enter the new one.""")


class CaptchaValidator(SimpleFieldValidator):
    """Captcha validator"""

    adapts(Interface, Interface, Interface, ICaptchaField, Interface)

    def validate(self, value):
        if self.widget.mode == HIDDEN_MODE:
            return True
        self.configlet = getUtility(ICaptchaConfiglet)
        if not self.configlet.verify(self.request):
            raise WrongCaptchaCode
        else:
            return True
