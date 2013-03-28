import logging
import random

from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from globals.auth_backends import general_login
from globals.utils import slugreverse, get_logger
from registration.forms import SignupForm, ResetPasswordForm
from registration.models import Registration
from registration.utils import check_username


# === Checked ===
def activate_user(request, activation_code):
    try:
        registration = Registration.objects.get_registration_obj_from_activation_code(activation_code)
        registration.gen_activation_code()
        new_user = registration.user
        new_user.is_active = True
        new_user.save()
        up = new_user.get_profile()

        registration.status = Registration.STATUS_COMPLETE
        registration.save()
        new_user.backend = 'django.contrib.auth.backends.ModelBackend'
        general_login(request, new_user)
    except Exception as e:
        log = get_logger('registration', level=logging.INFO)
        log.info("Activation failed, the error is: %s" % e)

    return redirect("/")


# === Checked ===
def reset_password(request, reset_code):
    '''
    When user clicks the reset link in the mail, bring the user to the reset password page
    '''
    
    registration = Registration.objects.get_registration_obj_from_activation_code(reset_code)
    
    if registration != False:
        user = registration.user
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                user.set_password(data.password)
                user.save()
                registration.gen_activation_code()
                print "Reset successfully"
                return redirect("/")
            else:
                print "Invalid form input"
        else:
            form = ResetPasswordForm()
            print "New password reset form"
    
        return render(request, "registration_reset_password.html", {
            'form': form,
        })
    else:
        return redirect("/")
