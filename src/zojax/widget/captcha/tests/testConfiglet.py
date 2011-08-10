import re
import string
from zojax.widget.captcha.config import LAYER_STATIC_CAPTCHAS, \
    PROPERTY_SHEET, LAYER_DYNAMIC_CAPTCHAS, PRODUCT_NAME

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password


class TestConfiglet(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.sp = self.portal.portal_properties.site_properties
        self.basic_auth = ':'.join((portal_owner, default_password))
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)

        self.capprops = self.portal.portal_properties[PROPERTY_SHEET]
        self.save_url = self.portal.id + \
            '/prefs_captchas_setup_form?form.submitted=1' + \
            '&form.button.form_submit=Save'

    def layerInSkins(self, layer):
        skins = self.portal.portal_skins
        for skin in skins.getSkinSelections():
            path = skins.getSkinPath(skin)
            path = map(string.strip, string.split(path, ','))
            if not layer in path:
                return False

        return True

    def test_staticOn(self):
        self.publish(self.save_url + '&static_captchas=static',
                     self.basic_auth)

        self.assertTrue(self.layerInSkins(LAYER_STATIC_CAPTCHAS),
            "No '%s' skin layer in some skins" % LAYER_STATIC_CAPTCHAS)

    def test_dynamicOn(self):
        self.publish(self.save_url + '&static_captchas=dynamic',
                     self.basic_auth).getBody()

        self.assertTrue(self.layerInSkins(LAYER_DYNAMIC_CAPTCHAS),
            "No '%s' skin layer in some skins" % LAYER_DYNAMIC_CAPTCHAS)

    def test_imageSize(self):
        expect = 35
        self.publish(self.save_url + '&image_size=%s' % expect,
             self.basic_auth)

        imsize = self.capprops.getProperty("image_size", 0)
        self.assertTrue(imsize == expect, '"image_size" property ' \
            'contains: "%s", must: "%s"' % (imsize, expect))

    def test_background(self):
        prop, expect = "background", "test-color"
        self.publish(self.save_url + '&%s=%s' % (prop, expect),
             self.basic_auth)

        fact = self.capprops.getProperty(prop, "")
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))

    def test_fontColor(self):
        prop, expect = "font_color", "test-font-color"
        self.publish(self.save_url + '&%s=%s' % (prop, expect),
             self.basic_auth)

        fact = self.capprops.getProperty(prop, "")
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))

    def test_period(self):
        prop, expect = "period", 22.3
        self.publish(self.save_url + '&%s=%s' % (prop, expect),
             self.basic_auth)

        fact = self.capprops.getProperty(prop, 0)
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))

    def test_amplitude(self):
        prop, expect = "amplitude", 11.2
        self.publish(self.save_url + '&%s=%s' % (prop, expect),
             self.basic_auth)

        fact = self.capprops.getProperty(prop, 0)
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))

    def test_random(self):
        prop, expect = "random_params", False
        self.publish(self.save_url, self.basic_auth)

        fact = self.capprops.getProperty(prop, None)
        self.assertTrue(fact == expect, '"%s" property ' \
            'contains: "%s", must: "%s"' % (prop, fact, expect))


class TestConfigletView(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)
        captcha_pref_path = self.portal.id + '/prefs_captchas_setup_form'
        basic_auth = portal_owner + ":" + default_password
        self.view = self.publish(captcha_pref_path, basic_auth).getBody()

    def matchinput(self, name):
        return re.match('.*<input\s+[^\>]*name=\"%s\"[^>]*>' % name,
                        self.view, re.I | re.S)

    def test_basic_form(self):
        reg_expr = '.*<form\s+[^\>]*action=\"[^\"]*?'\
                   'prefs_captchas_setup_form\"[^>]*>'
        form = re.match(reg_expr, self.view, re.I | re.S)
        self.assertNotEqual(form, None,
            "No 'Plone Captchas Setup' form present on the configlet view")
        self.assertNotEqual(self.matchinput('form\.button\.form_submit'), None,
            "No submit button on the form")
        self.assertNotEqual(self.matchinput('static_captchas'), None,
            "No static/dynamic radio button present on the configlet")

    def test_dynamic(self):
        params = ["image_size", "background", "font_color",
                  "period", "amplitude", "random_params"]
        for param in params:
            self.assertNotEqual(self.matchinput(param), None,
                "'%s' form element absence on the configlet form" % param)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestConfiglet))
    suite.addTest(makeSuite(TestConfigletView))
    return suite
