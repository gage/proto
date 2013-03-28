""" Site search module VIEW functions """

__author__ = "Jason Ke<jason.ke@geniecapital.com>"
__version__ = "$Id$"

from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from search.models import ScoreActionTable
from dish.models import Dish
from iptolocation.models import IPToLocation
from place.models import Place
from events.models import Event
from actstream.models import Action
from django.contrib.auth.models import User
from haystack.query import SearchQuerySet
from search.utils import personal_ranking, get_clear_search_results, spatial_ranking, get_user_location, name_seperate
from globals.utils import slugreverse
from math import ceil
import datetime
from haystack.query import SQ

TYPE = {
        'dish': [Dish],
        'place': [Place],
        'people': [User],
        'user': [User],
        'event': [Event],
#        'all': [Dish, Place],
        'non_spatial': [ User, Event ],
        'spatial': [Dish, Place],
        'all': [Dish, Place, User],
    }

DJANGO_CT = {
        'user': ['auth.user'],
        'event': ['events.event'],
        'non_spatial': ['auth.user', 'events.event'],
    }


def search(request):
    return redirect('registration-signup')
    if request.method == 'GET':
        input_q = request.GET.get("q","")
        q = name_seperate(input_q)
        default_num = 10
        #results = personal_ranking(s_qs=SearchQuerySet().auto_query(q).models(*TYPE['all']), user=request.user)        
        # Find location
        latitude, longitude = get_user_location(request)        
        search_city = request.session.get('search_city', 'Default')
        
        spatial_results = spatial_ranking(personal_ranking(SearchQuerySet().models(*TYPE['spatial']).filter(searchable=True), request.user), latitude, longitude).auto_query(q).load_all()[:default_num]
        spatial_results = get_clear_search_results(spatial_results)        
        
        results = personal_ranking(SearchQuerySet().models(*TYPE['non_spatial']).filter(searchable=True), request.user).load_all().auto_query(q)[:default_num]
        results = get_clear_search_results(results)
        
        results.extend(spatial_results)
        rtn = []
        for result in results:
            if result.pk not in request.user.get_profile().blocked_by_user_set:
                rtn.append(result)
                
        return render(request, 'search_result.html', {
            'results':rtn,
            'search_city':search_city,
            'q': input_q,
            'default_num': default_num,
        })
    else:
        return HttpResponseRedirect(slugreverse(request.user, "user-profile", args=[request.user.id]))
