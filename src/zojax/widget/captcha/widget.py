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

from zope.component import getUtility
from zope.interface import implementer

from z3c.form import interfaces, widget
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE
from z3c.pt.pagetemplate import ViewPageTemplateFile

from interfaces import ICaptchaConfiglet


class CaptchaWidget(TextWidget):

    captcha_template = ViewPageTemplateFile('widget.pt')

    def __init__(self, *kv, **kw):
        super(CaptchaWidget, self).__init__(*kv, **kw)
        self.configlet = getUtility(ICaptchaConfiglet)

    def captchaImage(self):
        return self.configlet.get_image_tag(self.request)

    def captchaAudio(self):
        return self.configlet.audio_url(self.request)

    def update(self):
        if self.mode == DISPLAY_MODE:
            self.mode = HIDDEN_MODE
            self.field.mode = interfaces.HIDDEN_MODE
        super(CaptchaWidget, self).update()

    def render(self):
        self.base_widget = super(CaptchaWidget, self).render()
        return self.captcha_template(self)


@implementer(interfaces.IFieldWidget)
def CaptchaWidgetFactory(field, request):
    return widget.FieldWidget(field, CaptchaWidget(request))
