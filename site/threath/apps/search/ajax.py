""" Site search module AJAX functions """
import threading

__author__ = "Jason Ke<u912538@gmail.com>"
__version__ = "$Id$"

import json, time
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.models import User
from dish.models import Dish
from globals.shortcuts import HttpJsonResponse
from place.models import Place
from haystack.query import SearchQuerySet
from search.utils import personal_ranking, get_clear_search_results, spatial_ranking, get_user_location, name_seperate, guess_language
from django.core.urlresolvers import reverse
from contact.models import Contact
from events.models import Event
from haystack.query import SQ
from fanjian.fanjian import zh_traditional, zh_simple

from search.utils import Ngram, process_query
from search.views import TYPE as SEARCH_TYPE, DJANGO_CT as SEARCH_DJANGO_CT

TYPE = SEARCH_TYPE
DJANGO_CT = SEARCH_DJANGO_CT


# For Contact AutoComplete
def auto_complete_people(request, selector='all'):
    """ people autocomplete
        indexes: first_name, last_name, email, phone, site_user
        type: 'all' (all), 'site' (site use only)
    """
    q = request.GET.get('q', None)
    selected = request.GET.get('selected', None)
    limit = request.GET.get('limit', 5)
    """ query handler """
    if q is None or q == '':
        return HttpResponse('', mimetype="text/plain")
    results = None
    has_query = False
    if not '@' in q:
        query_list = process_query(q)
        for q_o in query_list:
            if q_o:
                if not has_query:
                    has_query = True
                    results = SearchQuerySet().filter(SQ(first_name__startswith=q_o) | SQ(last_name__startswith=q_o) | \
                                 SQ(email__startswith=q_o) | SQ(phone__startswith=q_o) | SQ(site_user__startswith=q_o))
                else:
                    results = results.filter(SQ(first_name__startswith=q_o) | SQ(last_name__startswith=q_o) | \
                                 SQ(email__startswith=q_o) | SQ(phone__startswith=q_o) | SQ(site_user__startswith=q_o))
    else:
        has_query = True
        results = SearchQuerySet().auto_query(q)

    if has_query:
        if request.user.is_anonymous() and 'viewer_site_user' in request.session:
            site_user = request.session['viewer_site_user']
        else:
            site_user = request.user

        results = results.filter(user=site_user.pk).exclude(is_slave=True).models(Contact).load_all()
    else:
        results = []

    if selector == 'site' and has_query:
        results = results.filter(site_user__range=['*','*'])

    if selected and has_query:
        selected = json.loads(selected)
        for _key, value in selected.items():
            results = results.exclude(cid=value)

    if has_query:
        results = results.load_all()[:limit]
    else:
        results = []

    tmp_response = []
    for result in results:
        score = 0
        if not result:
            continue
        img_url = result.object.get_display_photo_url(size='26x26')
        img_url_l = result.object.get_display_photo_url(size='50x50')
        url = ''
        name = result.object.get_display_name()
        item = [
            result.pk,
            name,
            result.model_name,
            '%s' % score,
            url,
            img_url,
            img_url_l,
        ]
        tmp_response.append(item)
    # tmp_response.sort(key=lambda obj: obj[1].lower().startswith(q),reverse=True)
    response = ["|".join(r) for r in tmp_response]
    response_txt = '\n'.join(response)
    return HttpResponse(response_txt, mimetype="text/plain")

def auto_complete_event(request):
    """
        event autocomplete
    """
    raise Exception('Deprecated')
    return
    # q = request.GET.get('q', None)
    # limit = request.GET.get('limit', 10)

    # """ query handler """
    # if q is None or q == '':
    #     return HttpResponse('', mimetype="text/plain")

    # query_list = process_query(q)
    # results = None

    # has_query = False
    # for q_o in query_list:
    #     if q_o:
    #         if not has_query:
    #             has_query = True
    #             results = personal_ranking(s_qs=SearchQuerySet().filter(searchable=True).filter(name__startswith=q_o), user=request.user)
    #         else:
    #             results = results.filter(name__startswith=q_o)
    # if has_query:
    #     results = get_clear_search_results(results.models(Event).load_all()[:limit])
    # else:
    #     results = []

    # tmp_response = []
    # for result in results:

    #     score_field = '%s_d'%request.user.id
    #     score = result.__dict__[score_field] if score_field in result.__dict__ else 'x'
    #     img_url = result.object.get_display_photo().image26x26.url
    #     img_url_l = result.object.get_display_photo().image105x105.url
    #     url = result.object.get_absolute_url()
    #     name = result.object.get_display_name()
    #     if len(name) > 30:
    #         name = '%s..' % name[:30]
    #     item = [
    #         result.pk,
    #         name,
    #         result.model_name,
    #         '%s' % score,
    #         url,
    #         img_url,
    #         img_url_l,
    #     ]
    #     tmp_response.append(item)

    # response = ["|".join(r) for r in tmp_response]
    # response_txt = '\n'.join(response)
    # return HttpResponse(response_txt, mimetype="text/plain")

def auto_complete_dish(request, place_id):
    """ dish autocomplete given place id
    """
    raise Exception('Deprecated')
    return
    # q = request.GET.get('q', None)
    # limit = request.GET.get('limit', 10)

    # """ query handler """
    # if q is None or q == '':
    #     return HttpResponse('', mimetype="text/plain")
    # query_list = process_query(q)
    # results = None

    # has_query = False
    # for q_o in query_list:
    #     if q_o:
    #         if not has_query:
    #             has_query = True
    #             results = personal_ranking(s_qs=SearchQuerySet().filter(name__startswith=q_o, place=place_id), user=request.user)
    #         else:
    #             results = results.filter(name__startswith=q_o)
    # if has_query:
    #     results = get_clear_search_results( results.load_all()[:limit] )
    # else:
    #     results = []

    # tmp_response = []
    # for result in results:
    #     img_url = result.object.get_display_photo().image26x26.url
    #     url = result.object.get_absolute_url()
    #     name = result.object.get_display_name()
    #     if len(name) > 20:
    #         name = '%s..' % name[:20]
    #     item = [
    #         result.pk,
    #         name,
    #         result.model_name,
    #         url,
    #         img_url,
    #     ]
    #     tmp_response.append(item)
    # # tmp_response.sort(key=lambda obj: obj[1].lower().startswith(q),reverse=True)
    # response = ["|".join(r) for r in tmp_response]
    # response_txt = '\n'.join(response)
    # return HttpResponse(response_txt, mimetype="text/plain")


def auto_complete_place(request):
    """ place autocomplete
    """
    q = request.GET.get('q', None)
    params = request.GET.get('other_params', None)
    limit = request.GET.get('limit', 10)

    latlon = None

    if params:
        params = json.loads(params)
        if 'lat' in params and 'lon' in params:
            latlon = (float(params['lat']), float(params['lon']))

    """ query handler """
    if q is None or q == '':
        return HttpResponse('', mimetype="text/plain")

    query_list = process_query(q)
    results = None

    # handle = open("/tmp/search.log","w")
    # ISOTIMEFORMAT='%Y-%m-%d %X'
    if latlon:
        latitude, longitude = latlon
    else:
        latitude, longitude = get_user_location(request)
    # t = time.strftime( ISOTIMEFORMAT, time.localtime() )
    # handle.write('start search:%s\n'%t)
    has_query = False
    for q_o in query_list:
        if q_o:
            if not has_query:
                has_query = True
                results = personal_ranking(s_qs=SearchQuerySet().filter(name__startswith=q_o), user=request.user)
            else:
                results = results.filter(name__startswith=q_o)
    if has_query:
        results = get_clear_search_results( spatial_ranking(results.models(Place), latitude, longitude, pure_dist=True).load_all()[:limit] )
    else:
        results = []
    # t = time.strftime( ISOTIMEFORMAT, time.localtime() )
    # handle.write('end search:%s\n'%t)
    tmp_response = []
    for result in results:
        # t = time.strftime( ISOTIMEFORMAT, time.localtime() )
        # handle.write('result:%s\n'%t)
        score_field = '%s_d'%request.user.id
        score = result.__dict__[score_field] if score_field in result.__dict__ else 'x'
        img_url = result.object.get_display_photo().image26x26.url
        img_url_l = result.object.get_display_photo().image105x105.url
        url = result.object.get_absolute_url()
        name = result.object.get_display_name()
        category = result.object.category
        if len(name) > 30:
            name = '%s..' % name[:30]
        item = [
            result.pk,
            name,
            result.model_name,
            '%s' % score,
            url,
            img_url,
            img_url_l,
            category,
        ]
        tmp_response.append(item)
    # tmp_response.sort(key=lambda obj: obj[1].lower().startswith(q),reverse=True)
    # t = time.strftime( ISOTIMEFORMAT, time.localtime() )
    # handle.write('End of all:%s\n'%t)
    response = ["|".join(r) for r in tmp_response]
    response_txt = '\n'.join(response)
    return HttpResponse(response_txt, mimetype="text/plain")

# Main Search Bar AutoComplete
def auto_complete_main(request):
    """ main search input autocomplete
    """

    q = request.GET.get('q', None)
    """ query handler """
    if q is None or q == '':
        return HttpResponse('', mimetype="text/plain")

    query_list = process_query(q)
    results = None

    latitude, longitude = get_user_location(request)

    has_query = False
    for q_o in query_list:
        if q_o:
            if not has_query:
                has_query = True
                results = personal_ranking(s_qs=SearchQuerySet().filter(searchable=True).filter(SQ(name=q_o)|SQ(name__startswith=q_o)|SQ(nickname__startswith=q_o)), user=request.user)
                print results
            else:
                results = results.filter(SQ(name=q_o)|SQ(name__startswith=q_o)|SQ(nickname__startswith=q_o))

    search_results = {}

    def p_search(search_set, model_name):
        if model_name in ['event', 'user']:
            search_results[model_name]['result'] = get_clear_search_results(search_set.load_all()[:3])
        elif model_name in ['place', ]:
            search_results[model_name]['result'] = get_clear_search_results(spatial_ranking(search_set, latitude, longitude).load_all()[:3])

    MODELS_ORDER = ['place', 'user', 'event']
    for model in MODELS_ORDER:
        if has_query:
            search_set = results.models(*TYPE[model])
            search_results[model] = {}
            search_results[model]['thread'] = threading.Thread(target=p_search, args=(search_set, model))

    for model_search in search_results:
        search_results[model_search]['thread'].start()

    for model_search in search_results:
        search_results[model_search]['thread'].join()

    all_results = []

    for model in MODELS_ORDER:
        print search_results
        all_results.append(search_results[model]['result'])

    response = []
    for key in range(len(all_results)):
        tmp_response = []
        item = []
        num = 0
        for result in all_results[key]:
            if result.pk in request.user.get_profile().blocked_by_user_set:
                continue
            num = num+1
            if num == 1:
                response.append('title|%s' % MODELS_ORDER[key])
            score_field = 'rank_score'
            score = result.__dict__[score_field] if score_field in result.__dict__ else 'x'
            try:
                if result.model_name == 'user':
                    img_url = result.object.get_profile().get_my_photo(request).image50x50.url
                else:
                    img_url = result.object.get_display_photo().image50x50.url
            except:
                img_url = ''

            extra = ""

            if result.model_name == 'user':
                # name = result.object.username
                name = result.object.get_profile().get_nickname(request)
                url = result.object.get_profile().get_absolute_url()
            elif result.model_name == 'place':
                extra = result.object.address
                name = result.object.get_display_name()
                url = result.object.get_absolute_url()
            else:
                name = result.object.get_display_name()
                url = result.object.get_absolute_url()

            item = [
				result.pk,
				name,
				result.model_name,
				'%s' % score,
				url,
				img_url,
                extra,
			]
            tmp_response.append(item)
        # tmp_response.sort(key=lambda obj: obj[1].lower().startswith(q),reverse=True)
        response.extend(["|".join(r) for r in tmp_response])
    response_txt = '\n'.join(response)

    return HttpResponse(response_txt, mimetype="text/plain")

def auto_complete_best_known_for(request):
    pass

def auto_complete_name(request, model):

    q = request.GET.get('q', None)
    q = name_seperate(q)
    rid = request.GET.get('rid', '')
    if q is None or q == '':
        return HttpResponse(json.dumps({'error':'query empty'}), mimetype="application/json")
    q = q.lower()
    query_list = q.split(" ")
    results = None
    for q_o in query_list:
        if q_o:
            if not results:
                results = personal_ranking(s_qs=SearchQuerySet().filter(name__startswith=q_o), user=request.user)
                # results = SearchQuerySet().filter(name__startswith=q_o)
            else:
                results = results.filter(name__startswith=q_o)

    results = results.models(*TYPE[model])[:5]
    json_response = []
    for result in results:
        score_field = '%s_d'%request.user.id
        score = result.__dict__[score_field] if score_field in result.__dict__ else 'x'
        try:
            img_url = result.object.get_display_photo().image40x40.url
        except:
            img_url = 0
        if rid:
            if result.object.place.pk == rid:
                item = {
                    'value': result.pk,
                    'data': '%s' % (result.object.name),
                	'score': '%s' % (score),
                	'img_url': '%s' % (img_url),
                }
            else:
                continue
        else:
            item = {
                'value': result.pk,
                'data': '%s' % (result.object.name),
                'score': '%s' % (score),
                'img_url': '%s' % (img_url),
            }

        json_response.append(item)
        # json_response.sort(key=lambda obj: obj['data'].lower().startswith(q),reverse=True)

#   return HttpResponse(json.dumps(json_response), mimetype="application/json")
    result = '\n'.join(["%s|%s|%s|%s" % (item['data'],item['value'],item['score'],item['img_url']) for item in json_response])
    return HttpResponse(result, mimetype="application/html")


def reset_user_locaion(request):
    city_id = request.GET.get("c",None)
    city_name = request.GET.get("city_name",None)
    if city_id:
        latitude, longitude = get_user_location(request, city_id, reset=True, city_name=city_name)
        return HttpResponse(json.dumps({'latitude':latitude, 'longitude':longitude, 'status':True}), mimetype="application/json")
    else:
        return HttpResponse(json.dumps({'status':False}), mimetype="application/json")

# Search Filter
def search_filter(request):
    """
        the filter of search.
        return json with search result html
        {
            status: 1(success) or 0(fail),
            html: search results,
            more: 1(has more) or 0 (no more),
            msg: any msg,
        }
    """
    if request.is_ajax and request.GET:
        q = request.GET.get("q", "")
        model = request.GET.get("m", "")
        city_id = request.GET.get("c", "")
        city_name = request.GET.get("name", None)
        from_index = int(request.GET.get("n", ""))
        to_index= int(request.GET.get("to_n", ""))

        if q and model:
            latitude, longitude = get_user_location(request) if city_id == 'null' else get_user_location(request, city_id, reset=True, city_name=city_name)

            if model == 'all':
                spatial_results = spatial_ranking(personal_ranking(SearchQuerySet().models(*TYPE['spatial']).filter(searchable=True), request.user), latitude, longitude).auto_query(q).load_all()[from_index:to_index]
                spatial_results = get_clear_search_results(spatial_results)

                results = personal_ranking(SearchQuerySet().models(*TYPE['non_spatial']).filter(searchable=True), request.user).load_all().auto_query(q)[from_index:to_index]
                results = get_clear_search_results(results)

                results.extend(spatial_results)
            elif model not in DJANGO_CT:
                results = spatial_ranking(personal_ranking(SearchQuerySet().models(*TYPE[model]).filter(searchable=True), request.user), latitude, longitude).auto_query(q).load_all()[from_index:to_index]
                results = get_clear_search_results(results)
            else:
                results = personal_ranking(SearchQuerySet().models(*TYPE[model]).filter(searchable=True), request.user).load_all().auto_query(q)[from_index:to_index]
                results = get_clear_search_results(results)

            rtn = []
            for result in results:
                if result.pk not in request.user.get_profile().blocked_by_user_set:
                    rtn.append(result)

            search_result = render_to_string('inc_search_result.html',{
                 #'results': results[start:start+num]
                 'results': rtn
            }, context_instance = RequestContext(request))
            response = {
                'status' : 1,
                'html' : search_result,
                'more' : 1,
                'msg' : '',
                'search_city' : request.session.get('search_city', 'Default'),
            }
        else:
            response = {
                'status' : 0,
                'html' : '',
                'more' : 0,
                'msg' : 'error',
            }

        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        response = {
                'status' : 0,
                'html' : '',
                'more' : 0,
                'msg' : 'error',
            }
        return HttpResponse(json.dumps(response), mimetype="application/json")


def search_name(request, model):

    q_r = request.GET.get('q_r', None)
    q_l = request.GET.get('q_l', None)

    try:
        start = int(request.GET.get('start', 0))
        num = int(request.GET.get('num', 10))
    except:
        return HttpResponse(json.dumps({'error':'get parameter error'}), mimetype="application/json")

    if q_r or q_l:
        if q_r and q_l:
            results = SearchQuerySet().name_auto_query(Ngram.get([q_r],2)).filter(address=q_l).models(*TYPE[model])
        elif q_r:
            results = SearchQuerySet().name_auto_query(Ngram.get([q_r],2)).models(*TYPE[model])
        else:
            results = SearchQuerySet().filter(address=q_l).models(*TYPE[model])
    else:
        return HttpResponse(json.dumps({'error':'query empty'}), mimetype="application/json")

    more = '';
    if len(results[start+num:]) > 0:
        more = {
            'url' : reverse('search-name', args=[model]),
            'q_r' : q_r,
            'q_l' : q_l,
            'start' : start+num,
            'num' : num,
        }

    if request.GET.get('small') == 'true':
        search_result = render_to_string('inc_place_picker_results_small.html',{
             'results': results[start:start+num]
        }, context_instance = RequestContext(request))
    else:
        search_result = render_to_string('inc_place_picker_results.html',{
             'results': results[start:start+num]
        }, context_instance = RequestContext(request))

    response = {
            'status' : 1,
            'html' : search_result,
            'more' : more,
            'msg' : '',
        }

    return HttpResponse(json.dumps(response), mimetype="application/json")


# For Contact Linking
def related_contact(request, selector='all'):
    """ contact autocomplete
        indexes: first_name, last_name, email, phone, site_user
        type: 'all' (all), 'site' (site use only), 'no_site' (exclude site user)
    """
    q = request.GET.get('q', None)
    contact_id = request.GET.get('contact_id', None)
    limit = 5

    # Exclude already slaved contacts
    exclude_idl = list(Contact.objects.all_filter(master_contact=contact_id).values_list('id', flat=True))
    exclude_idl.append(contact_id)

    """ query handler """
    if q is None or q == '':
        return HttpJsonResponse()
    results = None
    has_query = False
    if not '@' in q:
        query_list = process_query(q)
        for q_o in query_list:
            if q_o:
                if not has_query:
                    has_query = True
                    results = SearchQuerySet().filter(SQ(first_name__startswith=q_o) | SQ(last_name__startswith=q_o) | \
                                 SQ(email__startswith=q_o) | SQ(phone__startswith=q_o) | SQ(site_user__startswith=q_o))
                else:
                    results = results.filter(SQ(first_name__startswith=q_o) | SQ(last_name__startswith=q_o) | \
                                 SQ(email__startswith=q_o) | SQ(phone__startswith=q_o) | SQ(site_user__startswith=q_o))
    else:
        has_query = True
        results = SearchQuerySet().auto_query(q)

    if has_query:
        results = results.filter(user=request.user.pk).exclude(is_slave=True).models(Contact).load_all()
    else:
        results = []

    if has_query:
        if selector == 'site':
            results = results.filter(site_user__range=['*','*'])
        elif selector == "no_site":
            results = results.exclude(site_user__range=['*','*'])
        results = results.exclude(cid__in=exclude_idl)
        results = results.load_all()[:limit]
    else:
        results = []

    tmp_response = []
    html_content = ""
    for result in results:
        # Use html to render the contact
        if not result:
            continue
        html_content += render_to_string('inc_contact_related.html', {'contact':result.object}, context_instance = RequestContext(request))
    data = {'html':html_content}
    return HttpJsonResponse(data)

