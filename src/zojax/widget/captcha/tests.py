import re
import unittest

from zope.interface import alsoProvides
from zope.schema.interfaces import IField
from zope.component import queryMultiAdapter
from zope.publisher.browser import TestRequest

from z3c.form import form
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IValidator
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IErrorViewSnippet

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import PloneTestCase as ptc

from zojax.widget.captcha.utils import *
from zojax.widget.captcha.tests.base import testPatch
from zojax.widget.captcha.tests.testWidget import addTestLayer

from zojax.widget.captcha import Captcha
from zojax.widget.captcha import CaptchaWidget
from zojax.widget.captcha import CaptchaWidgetFactory
from zojax.widget.captcha.validator import CaptchaValidator

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    # Register z3c namespace first (work before plone-3.3)
    import z3c.form
    zcml.load_config('meta.zcml', z3c.form)
    # Now register zojax.widget.captcha package
    import zojax.widget.captcha
    import zojax.widget.captcha
    zcml.load_config('configure.zcml', zojax.widget.captcha)
    fiveconfigure.debug_mode = False
    ztc.installPackage('zojax.widget.captcha')

setup_product()
ptc.setupPloneSite(extension_profiles=['zojax.widget.captcha:default',])


class TestRegistrations(ptc.PloneTestCase):

    def afterSetUp(self):
        self.request = self.app.REQUEST
        alsoProvides(self.request, IFormLayer)

    def testCaptchaFieldInterface(self):
        self.assertEqual(IField.implementedBy(Captcha), True)

    def testCaptchaWidgetInterface(self):
        self.assertEqual(IFieldWidget.implementedBy(CaptchaWidgetFactory), True)

    def testWidgetRegistration(self):
        cfield = Captcha()
        cwidget = queryMultiAdapter((cfield, self.request), IFieldWidget)
        self.assertNotEqual(cwidget, None)

    def testValidatorRegistration(self):
        cfield = Captcha()
        cvalidator = queryMultiAdapter((None, self.request, None, cfield, None),
                IValidator)
        self.assertNotEqual(cvalidator, None)

    def testErrorViewRegistration(self):
        cfield = Captcha()
        cwidget = queryMultiAdapter((cfield, self.request), IFieldWidget)
        error = ValueError()
        eview = queryMultiAdapter(
            (error, self.request, cwidget, cfield, None, None),
            IErrorViewSnippet)
        self.assertNotEqual(eview, None)


class TestCaptchaWidget(ptc.PloneTestCase):

    def afterSetUp(self):
        self.request = self.app.REQUEST
        alsoProvides(self.request, IFormLayer)

        cform = form.BaseForm(self.portal, self.request)
        cform.prefix = ""
        cwidget = CaptchaWidget(self.request)
        cwidget.form = cform
        self.html = cwidget.render()

    def testHidden(self):
        HIDDENTAG = '<input\s+[^>]*(?:' \
            '(?:type="hidden"\s*)|' \
            '(?:name="hashkey"\s*)|' \
            '(?:value="(?P<value>[0-9a-fA-F]+)"\s*)' \
            '){3}/>'
        open('/tmp/z3c.form.html','w').write(self.html)
        hidden = re.search(HIDDENTAG, self.html)
        self.assertTrue(hidden and hidden.group('value'))

    def testImg(self):
        IMAGETAG = '<img\s+[^>]*src=\"' \
            '(?P<src>[^\"]*/getCaptchaImage/[0-9a-fA-F]+)' \
            '\"[^>]*>'
        img = re.search(IMAGETAG, self.html)
        self.assertTrue(img and img.group('src'))

    def testTextField(self):
        FIELDTAG = '<input\s+[^>]*type=\"text\"\s*[^>]*>'
        self.assertEqual(re.search(FIELDTAG, self.html) is not None, True)
        

class TestCaptchaValidator(ptc.PloneTestCase):

    def afterSetUp(self):
        self.request = self.app.REQUEST
        alsoProvides(self.request, IFormLayer)
        # prepare context
        self.loginAsPortalOwner()
        testPatch()
        addTestLayer(self)
        self.captcha_key = self.portal.captcha_key
        # prepare captcha data
        self.hashkey = self.portal.getCaptcha()
        self.request.form['hashkey'] = self.hashkey
        # prepare validator
        cform = form.BaseForm(self.portal, self.request)
        cform.prefix = ""
        cwidget = CaptchaWidget(self.request)
        cwidget.form = cform
        self.validator = CaptchaValidator(self.portal, self.request, None, None, cwidget)

    def testSubmitRightCaptcha(self):
        decrypted = decrypt(self.captcha_key, self.hashkey)
        key = getWord(int(parseKey(decrypted)['key'])-1 )
        try:
            res = self.validator.validate(key)
        except ConversionError, e:
            self.fail("Rised unexpected %s error on right captcha submit" % e)

    def testSubmitWrongCaptcha(self):
        try:
            res = self.validator.validate("wrong key")
        except ValueError, e:
            self.assertEqual(str(e), u'Please re-enter validation code.')
        else:
            self.fail("No ValueError rised on wrong captcha key submit")

    def testSubmitRightCaptchaTwice(self):
        decrypted = decrypt(self.captcha_key, self.hashkey)
        key = getWord(int(parseKey(decrypted)['key'])-1 )
        self.validator.validate(key)
        try:
            res = self.validator.validate(key)
        except ValueError, e:
            self.assertEqual(str(e), u'Please re-enter validation code.')
        else:
            self.fail("No ValueError rised on right captcha key " \
                      "submitting twice")


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRegistrations))
    suite.addTest(unittest.makeSuite(TestCaptchaWidget))
    suite.addTest(unittest.makeSuite(TestCaptchaValidator))
    return suite
