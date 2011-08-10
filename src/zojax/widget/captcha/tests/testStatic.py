import string
import unittest
from zojax.widget.captcha.config import LAYER_STATIC_CAPTCHAS, \
    CAPTCHAS_COUNT, PRODUCT_NAME
from zojax.widget.captcha.utils import encrypt1, parseKey, decrypt, getWord

from Products.PloneTestCase import PloneTestCase as ptc

from DateTime import DateTime
from Products.CMFFormController.ControllerState import ControllerState


class TestStatic(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)
        self.skins = self.portal.portal_skins

        self.captcha_key = self.portal.captcha_key
        self.hashkey = self.portal.getCaptcha()

    def testStaticByDefault(self):
        # After installation static layer must present in all skin paths
        for skin in self.skins.getSkinSelections():
            path = self.skins.getSkinPath(skin)
            path = map(string.strip, string.split(path, ','))
            self.assertTrue(LAYER_STATIC_CAPTCHAS in path)

    def testImagesCount(self):
        # All images must present in static skin layer
        static = self.skins.restrictedTraverse('captchas')
        static_ids = static.objectIds()
        for i in range(1, CAPTCHAS_COUNT + 1):
            self.assertTrue("%s.jpg" % i in static_ids,
                            "No %s.jpg in static, %s" % (i, static_ids))

    def test_GetCaptcha_Date(self):
        # *date* must present after parsing decrypted key
        decrypted_key = decrypt(self.captcha_key, self.hashkey)
        parsed_key = parseKey(decrypted_key)
        self.assertTrue('date' in parsed_key.keys())

    def test_GetCaptcha_Key(self):
        decrypted_key = decrypt(self.captcha_key, self.hashkey)
        parsed_key = parseKey(decrypted_key)
        # *key* must present after parsing decrypted key
        self.assertTrue('key' in parsed_key.keys())
        # index start from 1 and lower or equals to CAPTCHAS_COUNT
        index = int(parsed_key['key'])
        self.assertTrue(index >= 1 and index <= CAPTCHAS_COUNT)
        # encrypted key must be equals to title of the image
        key = getWord(index - 1)
        img = getattr(self.portal, '%s.jpg' % index)
        self.assertTrue(encrypt1(key) == img.title)

    def test_GetImage(self):
        # getCaptchaImage function must return image coded in hashkey same to
        # image get by 'key' after parsing decrypted key
        req, resp = self.app.REQUEST, self.app.REQUEST.RESPONSE
        decrypted_key = decrypt(self.captcha_key, self.hashkey)
        parsed_key = parseKey(decrypted_key)
        img = self.portal.restrictedTraverse(parsed_key['key'] + '.jpg')
        img_html = img.index_html(req, resp)

        portal = self.portal.absolute_url(1)
        captcha_path = portal + "/getCaptchaImage/%s" % self.hashkey
        obj_html = self.publish(captcha_path).getBody()
        msg = "Image get by getCaptchaImage script is differ from"\
              "image get by index (after parsing decrypted key)"
        self.assertTrue(obj_html == img_html, msg)


class TestStaticValidator(ptc.PloneTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)
        self.captcha_key = self.portal.captcha_key
        # Preparation for validator tests
        self.pfc = self.portal.portal_form_controller
        self.req = self.app.REQUEST
        # set up a dummy state object
        self.dummycs = ControllerState(id='prefs_captchas_setup_form',
            context=self.portal, button='submit', status='success',
            errors={}, ext_action=None,)

    def testGoodData(self):
        hashkey = self.portal.getCaptcha()
        decrypted_key = decrypt(self.captcha_key, hashkey)
        key = getWord(int(parseKey(decrypted_key)['key']) - 1)
        self.req.form['hashkey'] = hashkey
        self.req.form['key'] = key + '1'

        cstate = self.pfc.validate(self.dummycs, self.req,
                                   ['captcha_validator', ])
        error_msg = 'Please re-enter validation code.'
        self.assertTrue(cstate.getErrors()['key'] == error_msg,
                        "Static captcha validator validate wrong key")

    def testBadKey(self):
        hashkey = self.portal.getCaptcha()
        self.req.form['hashkey'] = hashkey
        self.req.form['key'] = 'bad key'

        cstate = self.pfc.validate(self.dummycs, self.req,
                                   ['captcha_validator', ])
        error_msg = 'Please re-enter validation code.'
        self.assertTrue(cstate.getErrors()['key'] == error_msg,
                        "Static captcha validator validate wrong key")

    def testBadDate(self):
        # First path DateTime to get old dated hash
        origDTTT = DateTime.timeTime
        now = DateTime().timeTime()
        DateTime.timeTime = lambda s: now - float(3601)

        hashkey = self.portal.getCaptcha()

        decrypted_key = decrypt(self.captcha_key, hashkey)
        key = getWord(int(parseKey(decrypted_key)['key']) - 1)
        self.req.form['hashkey'] = hashkey
        self.req.form['key'] = key
        # Return original Date
        DateTime.timeTime = origDTTT
        cstate = self.pfc.validate(self.dummycs, self.req,
                                   ['captcha_validator', ])
        error_msg = 'Please re-enter validation code.'
        self.assertTrue(cstate.getErrors()['key'] == error_msg,
                        "Static captcha validator validate wrong key")


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStatic))
    suite.addTest(unittest.makeSuite(TestStaticValidator))
    return suite
