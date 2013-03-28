import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from globals.utils import bigpipe_pagelet


def verify_email(request):
    '''
    When user click the activation link, the email will be verified.
    '''
    activation_code = request.GET.get('activation_code')
    email = request.GET.get('email')
    uid = request.GET.get('id')

    # print "activation_code: %s" % activation_code
    # print "email: %s" % email
    # print "id: %s" % uid

    user = User.objects.get(id=uid)
    # print user

    profile = user.get_profile()

    if profile.verify_email(email, activation_code):
        return HttpResponse("Email has been verified successfully.")
    else:
        return HttpResponse("This activation code is expired.")

@login_required
def user_main(request, user_id=None):
    def stream_response_generator():
        context = {
            'BIG_PIPE': True
        }
        base_view = render_to_string("main.html", context, context_instance=RequestContext(request))
        yield base_view.ljust(4096)
        yield bp_testpagelet(request).ljust(4096)
        yield render_to_string("bp_page_end.html", {}, context_instance=RequestContext(request))

    return HttpResponse(stream_response_generator(), mimetype='text/html', stream_content=True)

@bigpipe_pagelet
def bp_testpagelet(request):
    innerHTML = render_to_string("bp_testpagelet.html", {'BIG_PIPE': True}, context_instance=RequestContext(request))
    return ['testpagelet',
            innerHTML,
            'chatRoom/chatRoom',
            ['base.css','test.css']
           ]





    
