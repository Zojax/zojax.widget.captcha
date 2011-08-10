from z3c.form import error
from zojax.widget.captcha import widget 

CaptchaFailureMessage = error.ErrorViewMessage(
    u'Please re-enter validation code.',
    error=ValueError,
    widget=widget.CaptchaWidget)
