from zope.interface import implementer
from z3c.pt.pagetemplate import ViewPageTemplateFile

from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser.text import TextWidget
import zope.component
from zope.app.component.hooks import getSite
from zope.traversing.browser.absoluteurl import absoluteURL

from interfaces import ICaptchaConfiglet

from zope.component import getUtility
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE


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
