## Controller Script (Python) "prefs_captchas_setup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Set necessary skin
##
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from zojax.widget.captcha.config import LAYER_DYNAMIC_CAPTCHAS
from zojax.widget.captcha.config import LAYER_STATIC_CAPTCHAS

import string

def exchangeLayers(layer1, layer2):
    for skin in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skin)
        path = map( string.strip, string.split( path,',' ))
        try:
            i = path.index(layer1)
            path.remove(layer1)
            path.insert(i, layer2)
        except ValueError:
            pass
        path = string.join( path, ', ' )
        skinstool.addSkinSelection( skin, path )

form = context.REQUEST.form
request_ids = form.keys()
ct = form.get('static_captchas')
skinstool = getToolByName(context, 'portal_skins')
if ct == 'static':
    exchangeLayers(LAYER_DYNAMIC_CAPTCHAS, LAYER_STATIC_CAPTCHAS)
else:
    exchangeLayers(LAYER_STATIC_CAPTCHAS, LAYER_DYNAMIC_CAPTCHAS)

captcha_props = getToolByName(context, 'portal_properties')['qPloneCaptchas']

property_map=[(m['id'], m['type']) for m in captcha_props.propertyMap() if not m['id']=='title']
kw={}
for id,type in property_map:
    if type == 'boolean':
        if id in request_ids:
            kw[id] = True
        else:
            kw[id] = False
    else:
        if id in request_ids:
            kw[id] = form[id]

captcha_props.manage_changeProperties(**kw)

context.plone_utils.addPortalMessage(_(u'Changes saved.'))
return state
