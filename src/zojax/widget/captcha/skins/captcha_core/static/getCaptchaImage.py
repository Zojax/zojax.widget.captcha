## Script (Python) "getCaptchaImage"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
from zojax.widget.captcha.utils import gen_captcha, decrypt, \
    getWord, parseKey

hk = context.REQUEST.traverse_subpath[0]
dk = decrypt(context.captcha_key, hk)
key = parseKey(dk)['key']
img = getattr(context, '%s.jpg' % key)
return img.index_html(context.REQUEST, context.REQUEST.RESPONSE)
