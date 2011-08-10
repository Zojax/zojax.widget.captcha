try:
    from App.class_init import InitializeClass
    InitializeClass
except ImportError:
    from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.Transience.Transience import TransientObjectContainer


class CaptchaTool(TransientObjectContainer):
    """portal_captcha tool class
    """
    meta_type = 'CaptchaTool'
    security = ClassSecurityInfo()
    security.declarePublic('addExpiredKey')

    def __init__(self, id='portal_captchas', title='',
                 timeout_mins=60, addNotification=None,
                 delNotification=None, limit=0, period_secs=60):
        TransientObjectContainer.__init__(self, id, title, timeout_mins,
                                          addNotification, delNotification,
                                          limit, period_secs)

    def addExpiredKey(self, key):
        self.new(key)

InitializeClass(CaptchaTool)
