## Script (Python) "getCaptchaType"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=actions=None
##title=
##
import string
from Products.CMFCore.utils import getToolByName
from zojax.widget.captcha.config import LAYER_DYNAMIC_CAPTCHAS
from zojax.widget.captcha.config import LAYER_STATIC_CAPTCHAS

skinsTool = getToolByName(context, 'portal_skins')
default_skin = skinsTool.getDefaultSkin()
path = skinsTool.getSkinPath(default_skin)
path = map(string.strip, string.split(path, ','))

if LAYER_STATIC_CAPTCHAS in path:
    return 'static'
elif LAYER_DYNAMIC_CAPTCHAS in path:
    return 'dynamic'
else:
    return None
