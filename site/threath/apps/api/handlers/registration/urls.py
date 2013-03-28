from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import SignupHandler, CheckUsernameHandler, CheckEmailHandler, CheckPasswordHandler, \
ResendAccountActivationCodeHandler, SendForgetPasswordEmailHandler,CheckFullnameHandler, ActivateHandler

urlpatterns = patterns('',
    url(r'^check_username/?$', Resource(handler=CheckUsernameHandler)),
    url(r'^check_fullname/?$', Resource(handler=CheckFullnameHandler)),
    url(r'^check_email/?$', Resource(handler=CheckEmailHandler)),
    url(r'^check_password/?$', Resource(handler=CheckPasswordHandler)),
    url(r'^signup/?$', Resource(handler=SignupHandler)),
    url(r'^activate/?$', Resource(handler=ActivateHandler)),
    # url(r'^singup_info/?$', Resource(handler=UserInfoHandler)),
    url(r'^resend_account_activation_code/?$', Resource(handler=ResendAccountActivationCodeHandler)),
    url(r'^send_forget_password_email/?$', Resource(handler=SendForgetPasswordEmailHandler)),

    # url(r'^complete_registration/?$', Resource(handler=CompleteRegistrationHandler)),
)
