## Script (Python) "getCaptcha"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
from zojax.widget.captcha.utils import getCaptchasCount, formKey, encrypt

from random import randint
# *randint* return random integer in range [a, b],
# including *both* end points.
key = formKey(randint(0, getCaptchasCount(True) - 1))
encrypted_key = encrypt(context.captcha_key, key)

return encrypted_key
