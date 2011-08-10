import transaction
from Products.CMFCore.utils import getToolByName


def uninstall(self):
    portal_setup = getToolByName(self, 'portal_setup')
    profile = "profile-zojax.widget.captcha:uninstall"
    portal_setup.runAllImportStepsFromProfile(profile, purge_old=False)
    transaction.savepoint()
