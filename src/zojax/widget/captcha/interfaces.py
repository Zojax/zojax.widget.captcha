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

from zope import interface, schema
from zope.i18n import MessageFactory

_ = MessageFactory('zojax.widget.captcha')


class ICaptchaConfiglet(interface.Interface):

    recaptchaPublicKey = schema.TextLine(
        title=_(u'Recaptcha Site key'),
        default=u'6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI',
        required=True)

    recaptchaPrivateKey = schema.TextLine(
        title=_(u'Recaptcha Secret key'),
        default=u'6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe',
        required=True)


class ICaptchaField(schema.interfaces.IASCIILine):
    """A field for captcha validation"""
