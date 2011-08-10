import unittest
from zojax.widget.captcha.config import LAYERS, LAYER_STATIC_CAPTCHAS, \
    PROPERTY_SHEET, CONFIGLET_ID, TOOL_ID, CAPTCHA_KEY, PRODUCT_NAME

from Products.PloneTestCase import PloneTestCase as ptc
from Products.CMFCore.utils import getToolByName


class TestInstallation(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = getToolByName(self.portal, 'portal_quickinstaller', None)
        self.cp = getToolByName(self.portal, 'portal_controlpanel', None)
        self.st = getToolByName(self.portal, 'portal_skins', None)
        self.qi.installProduct(PRODUCT_NAME)

    def getLayers(self):
        return LAYERS + [LAYER_STATIC_CAPTCHAS]

    def testPropertysheetInstall(self):
        pp = getToolByName(self.portal, 'portal_properties')
        msg = 'Property sheet isn\'t found'
        self.assert_(PROPERTY_SHEET in pp.objectIds(), msg)

    def testPropertysheetUninstall(self):
        self.qi.uninstallProducts([PRODUCT_NAME])
        pp = getToolByName(self.portal, 'portal_properties')
        self.assert_(not PROPERTY_SHEET in pp.objectIds(),
            'Property sheet found after uninstallation')

    def testConfigletInstall(self):
        list_ids = []
        for action in self.cp.listActions():
            list_ids.append(action.getId())
        self.assert_(CONFIGLET_ID in list_ids, 'Configlet not found')

    def testConfigletUninstall(self):
        self.qi.uninstallProducts([PRODUCT_NAME])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT_NAME), True,
                            '%s is already installed' % PRODUCT_NAME)
        list_ids = []
        for action in self.cp.listActions():
            list_ids.append(action.getId())
        msg = 'Configlet found after uninstallation'
        self.assert_(not CONFIGLET_ID in list_ids, msg)

    def testSkinsInstall(self):
        skinstool = self.st
        layers = self.getLayers()
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(str.strip, path.split(','))
            for layer in layers:
                msg = '%s directory view not found in'\
                      'portal_skins after installation' % layer
                self.assert_(layer.split('/')[0] in skinstool.objectIds(), msg)
                msg = '%s layer not found in %s' % (PRODUCT_NAME, skin)
                self.assert_(layer in path, msg)

    def testSkinsUninstall(self):
        self.qi.uninstallProducts([PRODUCT_NAME])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT_NAME), True,
                            '%s is already installed' % PRODUCT_NAME)
        skinstool = self.st
        layers = self.getLayers()
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(str.strip, path.split(','))
            for layer in layers:
                msg = '%s directory view found in'\
                      'portal_skins after uninstallation' % layer
                skins_tool_ids = skinstool.objectIds()
                self.assert_(not layer.split('/')[0] in skins_tool_ids, msg)
                msg = '%s layer found in'\
                      '%s after uninstallation' % (layer, skin)
                self.assert_(not layer in path, msg)

    def testToolInstall(self):
        self.assert_(TOOL_ID in self.portal.objectIds())

    def testToolUninstall(self):
        self.qi.uninstallProducts([PRODUCT_NAME])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT_NAME), True,
            '%s is already installed' % PRODUCT_NAME)
        self.assert_(not TOOL_ID in self.portal.objectIds())

    def testCaptchaKey(self):
        ck = getattr(self.portal, CAPTCHA_KEY)
        self.assert_(ck)
        self.assertEqual(len(ck), 8)
        self.qi.uninstallProducts([PRODUCT_NAME])
        self.assert_(not self.portal.hasProperty(CAPTCHA_KEY))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInstallation))
    return suite
