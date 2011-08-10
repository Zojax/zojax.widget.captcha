from Products.CMFCore.utils import getToolByName

from zojax.widget.captcha import ProductMessageFactory as _
from zojax.widget.captcha.utils import decrypt, parseKey, \
    encrypt1, getWord
from DateTime import DateTime

if state.getStatus()=='failure':
    return  state
request = context.REQUEST

test_key = request.get('key', '')
hashkey = request.get('hashkey', '')
decrypted_key = decrypt(context.captcha_key, hashkey)
parsed_key = parseKey(decrypted_key)

index = parsed_key['key']
date = parsed_key['date']

img = getattr(context, '%s.jpg' % index)
solution = img.title
enc = encrypt1(test_key)
captcha_tool = getToolByName(context, 'portal_captchas')
if (enc != solution) or (captcha_tool.has_key(decrypted_key)) \
    or (DateTime().timeTime() - float(date)>3600):
    message = _(u"Please re-enter validation code.")
    context.plone_utils.addPortalMessage(message, 'error')
    state.setError('key', message, 'key_required')
    return state.set(status="failure")
else:
    captcha_tool.addExpiredKey(decrypted_key)
    return state.set(status="success")
