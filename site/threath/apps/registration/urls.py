""" Registration URLs """

from django.conf.urls.defaults import *

urlpatterns = patterns('registration.views',
    # url(r'^signup/$', 'signup', name="registration-signup"),
    url(r'^activate/(?P<activation_code>\w+)/$', 'activate_user', name="activate-user"),
    url(r'^reset_password/(?P<reset_code>\w+)/$', 'reset_password', name="reset-password"),
)

urlpatterns += patterns('registration.ajax',
    url(r'^ajax/send_reset_password_mail/$','ajax_send_reset_password_mail', name="ajax-send-reset-password-mail"),
    url(r'^ajax/process_sign_up_form/$','ajax_process_sign_up_form', name="ajax-process-sign-up-form"),
    url(r'^ajax/send_activation_mail/(?P<registration_id>\w+)/$','ajax_send_activation_mail', name="ajax-send-activation-mail"),
    url(r'^ajax/check_username/$','ajax_check_username', name="ajax-check-username"),
)
