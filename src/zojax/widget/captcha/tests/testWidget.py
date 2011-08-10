import re
import string
import unittest
from zojax.widget.captcha.config import PRODUCT_NAME, GLOBALS
from base import testPatch
from zojax.widget.captcha.utils import getWord, decrypt, parseKey

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.PloneTestCase import portal_owner
from Products.PloneTestCase.PloneTestCase import default_password

from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.DirectoryView import addDirectoryViews

NOT_VALID = re.compile("Please re\-enter validation code")
IMAGE_PATT = '\s+src="%s(/getCaptchaImage/[0-9a-fA-F]+)"'

# patch to use test images and dictionary
testPatch()


def addTestLayer(self):
    # Install test_captcha skin layer
    registerDirectory('tests', GLOBALS)
    skins = self.portal.portal_skins
    addDirectoryViews(skins, 'tests', GLOBALS)
    skinName = skins.getDefaultSkin()
    paths = map(string.strip, skins.getSkinPath(skinName).split(','))
    paths.insert(paths.index('custom') + 1, 'test_captcha')
    skins.addSkinSelection(skinName, ','.join(paths))
    self._refreshSkinData()


class TestCaptchaWidget(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.addProduct(PRODUCT_NAME)
        addTestLayer(self)
        self.portal.invokeFactory('Document', 'index_html')
        self.portal['index_html'].allowDiscussion(True)
        self.absolute_url = self.portal['index_html'].absolute_url_path()

        self.basic_auth = ':'.join((portal_owner, default_password))
        self.captcha_key = self.portal.captcha_key

    def testImage(self):
        path = '%s/test_form' % self.absolute_url
        response = self.publish(path, self.basic_auth,
                                request_method='GET').getBody()
        patt = re.compile(IMAGE_PATT % self.portal.absolute_url())
        match_obj = patt.search(response)

        img_url = match_obj.group(1)
        res = self.publish('/plone' + img_url, self.basic_auth)
        content_type = res.getHeader('content-type')
        self.assert_(content_type.startswith('image'))

    def testSubmitRightCaptcha(self):
        hashkey = self.portal.getCaptcha()
        # index of word number starts from 1,
        # but index of dictionary starts from 0
        decrypted_key = decrypt(self.captcha_key, hashkey)
        key = getWord(int(parseKey(decrypted_key)['key']) - 1)
        parameters = 'form.submitted=1&key=%s' % key
        path = '%s/test_form?%s' % (self.absolute_url, parameters)
        extra = {'hashkey': hashkey,
                 'form.button.Save': 'Save'}
        response = self.publish(path, self.basic_auth, extra=extra,
                                request_method='GET').getBody()
        self.assert_(not NOT_VALID.search(response))

    def testSubmitWrongCaptcha(self):
        hashkey = self.portal.getCaptcha()
        parameters = 'form.submitted=1&key=fdfgh'
        path = '%s/test_form?%s' % (self.absolute_url, parameters)
        extra = {'hashkey': hashkey,
                 'form.button.Save': 'Save'}
        response = self.publish(path, self.basic_auth, extra=extra,
                                request_method='GET').getBody()
        self.assert_(NOT_VALID.search(response))

    def testSubmitRightCaptchaTwice(self):
        hashkey = self.portal.getCaptcha()
        decrypted_key = decrypt(self.captcha_key, hashkey)
        key = getWord(int(parseKey(decrypted_key)['key']) - 1)
        parameters = 'form.submitted=1&key=%s' % key
        path = '%s/test_form?%s' % (self.absolute_url, parameters)
        extra = {'hashkey': hashkey,
                 'form.button.Save': 'Save'}
        self.publish(path, self.basic_auth, extra=extra, request_method='GET')
        response = self.publish(path, self.basic_auth, extra=extra,
                                request_method='GET').getBody()

        self.assert_(NOT_VALID.search(response))

    def testCaptchaWidget(self):
        # captcha core related issue, described in
        # in http://plone.org/products/plone-comments/issues/5
        resp = self.publish(self.portal.absolute_url(1) + "/captcha_widget")
        self.assertEqual(resp.status / 100, 2)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCaptchaWidget))
    return suite
