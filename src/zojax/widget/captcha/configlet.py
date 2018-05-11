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

import urllib2
import urllib
import logging

from zope import schema
from zope.annotation.factory import factory
from zope.component import adapts  # , getUtility
from zope.interface import implements
from zope.interface.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest

from zojax.resourcepackage.library import includeInplaceSource

from interfaces import ICaptchaConfiglet

try:
    import simplejson as json
except ImportError:
    import json

logger = logging.getLogger('zojax.widget.captcha')


class IRecaptchaInfo(Interface):
    error = schema.TextLine()
    verified = schema.Bool()


class RecaptchaInfoAnnotation(object):
    implements(IRecaptchaInfo)
    adapts(IBrowserRequest)

    def __init__(self):
        self.error = None
        self.verified = False
RecaptchaInfo = factory(RecaptchaInfoAnnotation)


class RecaptchaResponse(object):

    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code


def displayhtml(public_key):
    includeInplaceSource(
        "<script src='https://www.google.com/recaptcha/api.js'></script>")

    return '<div class="g-recaptcha" data-sitekey="%(PublicKey)s"></div>' % {
        'PublicKey': public_key, }


def submit(recaptcha_response_field, private_key, remoteip):
    if not (recaptcha_response_field and len(recaptcha_response_field)):
        return RecaptchaResponse(is_valid=False, error_code='invalid-response')

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode({
        'secret': encode_if_necessary(private_key),
        'response': encode_if_necessary(recaptcha_response_field),
        'remoteip': encode_if_necessary(remoteip),
    })

    request = urllib2.Request(
        url="https://www.google.com/recaptcha/api/siteverify",
        data=params,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
        }
    )

    result = json.loads(urllib2.urlopen(request).read())

    if result['success']:
        return RecaptchaResponse(is_valid=True)
    else:
        return RecaptchaResponse(is_valid=False,
                                 error_code=result['error-codes'])


class CaptchaConfiglet(object):
    """configlet for captchas"""

    implements(ICaptchaConfiglet)

    NOT_CONFIGURED_MESSAGE = 'No recaptcha public key configured. Go to path/to/site/settings to configure.'

    def get_image_tag(self, request):
        if not self.recaptchaPublicKey:
            logger.warning()
            return "<p>%s<p>" % self.NOT_CONFIGURED_MESSAGE

        return displayhtml(self.recaptchaPublicKey)

    def audio_url(self):
        return None

    def verify(self, request, input=None):
        info = IRecaptchaInfo(request)
        if info.verified:
            return True

        if not self.recaptchaPrivateKey:
            raise ValueError(self.NOT_CONFIGURED_MESSAGE)
        response_field = request.get('g-recaptcha-response')
        remote_addr = request.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
        if not remote_addr:
            remote_addr = request.get('REMOTE_ADDR')

        res = submit(response_field, self.recaptchaPrivateKey, remote_addr)

        if res.error_code:
            info.error = res.error_code

        info.verified = res.is_valid
        return res.is_valid
