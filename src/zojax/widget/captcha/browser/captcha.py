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
from zope.app.file.image import Image
from zope.app.component.hooks import getSite
from zope.traversing.api import traverse
"""

$Id$
"""
from zope import interface
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces import IPublishTraverse
from zope.security.proxy import removeSecurityProxy
from zope.component import getAdapters, queryMultiAdapter, getUtility

from zojax.widget.captcha.interfaces import ICaptchaConfiglet
from zojax.widget.captcha.utils import gen_captcha, decrypt, \
    getWord, parseKey
import random


class GetCaptchaImage(object):

    interface.implements(IPublishTraverse)

    __name__ = 'getCaptchaImage'
    __parent__ = None

    def __init__(self, context, request):
        self.__parent__ = self.context = context
        self.request = request
        self.configlet = getUtility(ICaptchaConfiglet)
        
    def publishTraverse(self, request, name):
        context = self.context
        configlet = self.configlet
        if configlet.type == 'dynamic':
            hk = name
            dk = decrypt(configlet.captchaKey, hk)
            key = parseKey(dk)['key']
            
            text = getWord(int(key), letters=configlet.letters, digits=configlet.digits, length=configlet.length)
            size = configlet.imageSize
            bkground = configlet.background
            font_color = configlet.fontColor
            kwargs = {'text': text,
                      'size': size,
                      'bkground': bkground,
                      'font_color': font_color}
            if configlet.randomParams:
                period = random.uniform(0.05, 0.12)
                amplitude = random.uniform(3.0, 6.5)
            else:
                period = configlet.period
                amplitude = configlet.amplitude
            
            kwargs['distortion'] = [period, amplitude, (0.0, 0.0)]
            kwargs['noise'] = configlet.noise
            
            im = gen_captcha(**kwargs)
            request.response.setHeader('Content-Type', 'image/jpeg')
            request.response.setHeader('Content-Length', im['size'])
            request.response.setHeader('Accept-Ranges', 'bytes')
            return Image(im['src'])
        else:
            hk = name
            dk = decrypt(configlet.captchaKey, hk)
            key = parseKey(dk)['key']
            return traverse(getSite(), '/@@/zojax-widget-captcha/captchas/%s.jpg' % key, request=request)
        raise NotFound(self.context, name, request)

