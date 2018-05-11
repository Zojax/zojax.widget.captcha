##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id$
"""

from zope.component import adapts
from zope.component._api import getUtility
from zope.interface import Interface
from zope.i18n import MessageFactory
from zope.schema import ValidationError

from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.validator import SimpleFieldValidator

from interfaces import ICaptchaField, ICaptchaConfiglet


_ = MessageFactory('zojax.widget.captcha')


class WrongCaptchaCode(ValidationError):
    __doc__ = _("""Invalid CAPTCHA. Please try again.""")


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
