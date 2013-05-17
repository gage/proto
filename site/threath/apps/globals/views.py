from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, render_to_response
from django.utils import simplejson
from django.conf import settings

from globals.utils import slugreverse


# Main App
def home(request):
    if not request.user.is_authenticated():
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'MSIE' in user_agent:
            if request.GET.get('landing'):
                return landing(request)
            else:
                return signup(request)
        return landing(request)
    else:
        current_user_ctx = simplejson.dumps(request.user.to_json())
        context = {
            'currentUser': current_user_ctx
        }
        return render_to_response("main.html", context, context_instance=RequestContext(request))


# Signup App
def signup(request):
    current_user_ctx = {}
    if request.user.is_authenticated():
        return HttpResponsePermanentRedirect(reverse('globals-home'))
    context = {
        'currentUser': current_user_ctx,
        'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
    }
    return render_to_response("signup/main.html", context, context_instance=RequestContext(request))


def landing(request):
    context = {}
    return render_to_response("landing_page.html", context, context_instance=RequestContext(request))


def render_tpl(request, template):
    try:
        return render_to_response(template, {}, context_instance=RequestContext(request))
    except:
        return render_to_response('page_not_found.html', {}, context_instance=RequestContext(request))


def globals_logout(request):
    logout(request)
    return redirect("/")