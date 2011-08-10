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
from Products.CMFCore.utils import getToolByName
import random
propTool = getToolByName(context, 'portal_properties')
captchaProps = propTool['qPloneCaptchas']

hk = context.REQUEST.traverse_subpath[0]
dk = decrypt(context.captcha_key, hk)
key = parseKey(dk)['key']

text = getWord(int(key))
size = captchaProps.getProperty('image_size')
bkground = captchaProps.getProperty('background')
font_color = captchaProps.getProperty('font_color')
kwargs = {'text': text,
          'size': size,
          'bkground': bkground,
          'font_color': font_color}
if captchaProps.getProperty('random_params', 'False'):
    period = random.uniform(0.05, 0.12)
    amplitude = random.uniform(3.0, 6.5)
else:
    period = captchaProps.getProperty('period')
    amplitude = captchaProps.getProperty('amplitude')

kwargs['distortion'] = [period, amplitude, (0.0, 0.0)]

im = gen_captcha(**kwargs)
context.REQUEST.RESPONSE.setHeader('Content-Type', 'image/jpeg')
context.REQUEST.RESPONSE.setHeader('Content-Length', im['size'])
context.REQUEST.RESPONSE.setHeader('Accept-Ranges', 'bytes')
return im['src']
