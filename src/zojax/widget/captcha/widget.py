from zope.interface import implementer
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form import interfaces
from z3c.form import widget

from z3c.form.browser.text import TextWidget
from zope.app.component.hooks import getSite
from zope.traversing.browser.absoluteurl import absoluteURL

from utils import getCaptchasCount, formKey, encrypt
from interfaces import ICaptchaConfiglet

from random import randint
from zope.component._api import getUtility
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE
     
class CaptchaWidget(TextWidget):
    
    def __init__(self, *kv, **kw):
        super(CaptchaWidget, self).__init__(*kv, **kw)
        self.configlet = getUtility(ICaptchaConfiglet)
        
    def update(self):
        if self.mode == DISPLAY_MODE:
            self.mode = HIDDEN_MODE
            self.field.mode = interfaces.HIDDEN_MODE
        super(CaptchaWidget, self).update()
    
    def getCaptcha(self):
        # *randint* return random integer in range [a, b],
        # including *both* end points.
        if self.configlet.type == 'dynamic':
            key = formKey(randint(0, getCaptchasCount(True) - 1))
        else:
            key = formKey(randint(1, getCaptchasCount(False)))
        return encrypt(self.configlet.captchaKey, key)

    def render(self):
        key = self.getCaptcha()
        portal_url = absoluteURL(getSite(), self.request)
        image_url = "%s/getCaptchaImage/%s"%(portal_url, key)
        
        if self.mode == HIDDEN_MODE:
            # Enforce template and do not query it from the widget template factory
            return ''
        self.value = ''
        return u"""<input type="hidden" value="%s" name="%shashkey" />
                    %s
                    <img src="%s" alt="Enter the word"/>""" % (key,
                                                               self.form.prefix,
                                                               super(CaptchaWidget, self).render(),
                                                               image_url)
        return super(CaptchaWidget, self).template(self) 


@implementer(interfaces.IFieldWidget)
def CaptchaWidgetFactory(field, request):
    return widget.FieldWidget(field, CaptchaWidget(request))
