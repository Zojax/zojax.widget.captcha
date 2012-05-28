from zojax.content.type.configlet import ContentContainerConfiglet
from zope.interface import implements
from zojax.language.interfaces import ISiteLanguage
from zope.annotation.factory import factory
from zope.component import getUtility, adapts
from recaptcha.client.captcha import displayhtml, submit
from zope import schema
from zope.interface.interface import Interface

from interfaces import ICaptchaConfiglet
import BTrees
from zope.publisher.interfaces.browser import IBrowserRequest

class IRecaptchaInfo(Interface):
    error = schema.TextLine()
    verified = schema.Bool()

class RecaptchaInfoAnnotation(object):
    implements(IRecaptchaInfo)
    adapts(IBrowserRequest)
    def __init__(self):
        self.error = None
        self.verified = False
RecaptchaInfo = factory(RecaptchaInfoAnnotation)

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


    def get_image_tag(self, request):
        lang = getUtility(ISiteLanguage).language
        options = """
        <script>
        var RecaptchaOptions = {
            lang: '%s'
        };
        </script>
        """ % lang

        if not self.recaptchaPublicKey:
            raise ValueError, 'No recaptcha public key configured. Go to path/to/site/@@recaptcha-settings to configure.'
        use_ssl = request['HTTPS'] == 'on'
        error = IRecaptchaInfo(request).error
        return options + displayhtml(self.recaptchaPublicKey, use_ssl=use_ssl, error=error)

    def audio_url(self):
        return None

    def verify(self, request, input=None):
        info = IRecaptchaInfo(request)
        if info.verified:
            return True

        if not self.recaptchaPrivateKey:
            raise ValueError, 'No recaptcha private key configured. Go to path/to/site/@@recaptcha-settings to configure.'
        challenge_field = request.get('recaptcha_challenge_field')
        response_field = request.get('recaptcha_response_field')
        remote_addr = request.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
        if not remote_addr:
            remote_addr = request.get('REMOTE_ADDR')
        res = submit(challenge_field, response_field, self.recaptchaPrivateKey, remote_addr)
        if res.error_code:
            info.error = res.error_code

        info.verified = res.is_valid
        return res.is_valid