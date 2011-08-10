from zope.interface import implementer
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form import interfaces
from z3c.form import widget

from Products.CMFCore.utils import getToolByName

from z3c.form.browser.text import TextWidget

class CaptchaWidget(TextWidget):
    
   def getCaptcha(self):
       return self.form.context.getCaptcha()

   def render(self):
       key = self.getCaptcha()
       portal_url = getToolByName(self.form.context, 'portal_url')()
       image_url = "%s/getCaptchaImage/%s"%(portal_url, key)

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
