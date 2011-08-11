from zojax.content.type.configlet import ContentContainerConfiglet
from zope.interface import implements

from interfaces import ICaptchaConfiglet
import BTrees


class CaptchaConfiglet(object):
    """configlet for captchas"""

    implements(ICaptchaConfiglet)
    
    family = BTrees.family32
    
    @property
    def records(self):
        data = self.data.get('records')
        if data is None:
            data = self.family.OO.BTree()
            self.data['records'] = data
        return data
    
    def addExpiredKey(self, key):
        self.records[key] = key
    
    def has_key(self, key):
        return self.records.has_key(key)