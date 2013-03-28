# -*- coding: UTF-8 -*-
""" Site search utility functions """

__author__ = "Gage Tseng <gage.tseng@gmail.com>"

import urllib2, urllib
import ngram

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from haystack.query import SearchQuerySet
from iptolocation.models import IPToLocation

from haystack.utils.geo import Point, D

#km
INIT_SEARCH_DELTA = 100
INDEX_LIST = ['name', 'text', 'rank_score', 'latlon', 'nickname', 'email', 'searchable', 'site_user']


class Ycas(object):

    data = {
        'appid': 'UX6cKNbV34GjjMw.H1BE89viP3yVUqGZmtM0u6c.BHFWhwCOirOq2DuR1QmH4gNw',
        'format': 'json',
        'content': '',
    }
    urlws = 'http://asia.search.yahooapis.com/cas/v1/ws'

    def ws(content):
        Ycas.data['content'] = content
        f = urllib2.urlopen(Ycas.urlws, urllib.urlencode(Ycas.data))
        return f.read()

    ws = staticmethod(ws)


# Todo: reexamine this, haystack has built-in ngram terms
class Ngram(object):

    def get(terms, n=5):

        # Todo: dirty hack
        src = " "
        for term in terms:
            if term is not None:
                src += term + " "
        src = src.strip()
        ws = []

        for i in range(n):
            index = ngram.NGram(N=i + 1)
            ws.extend(list(index.ngrams(src)))

        set_var = {}
        map(set_var.__setitem__, ws, [])
        ws = set_var.keys()

        wsstr = ''
        for o in ws:
            wsstr += o.replace('$', '') + ' '
        wsstr = wsstr.rstrip()
#       print wsstr
        return wsstr

    get = staticmethod(get)


def process_query(q):
    """Process user query for auto-complete start-with query."""
    q = '%s' % q
    q = name_seperate(q)
    q = q.lower()
    replace_str = "-'_@!&,./;:[](){}+=*^%$#~`?<>|"
    for char in replace_str:
        q = q.replace(char, ' ')
    q = q.strip()
    # Process Digital
    # q = digit_seperate(q)
    query_list = q.split(" ")
    query_list = list(set(query_list))
    if '' in query_list:
        query_list.remove('')
    return query_list


def word_analize(str_o):
    rtn_str = ''
    uni_name = unicode(str_o)
    record_ind = 0
    last_dict = {'isChinese': False, 'ptr': -1}
    this_dict = {'isChinese': False, 'ptr': 0}
    for c in uni_name:
        this_dict['isChinese'] = True if (c >= u'\u4e00' and c <= u'\u9fa5') else False
        if last_dict['ptr'] == -1:
            last_dict['isChinese'] = this_dict['isChinese']
        if this_dict['isChinese'] != last_dict['isChinese']:
            if last_dict['isChinese']:
                # Do Chinese Ngram
                rtn_str += Ngram.get([str_o[record_ind:this_dict['ptr']]]) + ' '
            else:
                rtn_str += str_o[record_ind:this_dict['ptr']] + ' '
            record_ind = this_dict['ptr']
        # Move forward one step
        last_dict['isChinese'] = this_dict['isChinese']
        last_dict['ptr'] = this_dict['ptr']
        this_dict['ptr'] += 1
    if last_dict['isChinese']:
        rtn_str += Ngram.get([str_o[record_ind:]])
    else:
        rtn_str += str_o[record_ind:]
    return rtn_str


def name_seperate(str_o):
    rtn_str = ''
    uni_name = unicode(str_o)
    record_ind = 0
    last_dict = {'isChinese': False, 'ptr': -1}
    this_dict = {'isChinese': False, 'ptr': 0}
    for c in uni_name:
        this_dict['isChinese'] = True if (c >= u'\u4e00' and c <= u'\u9fa5') else False
        if last_dict['ptr'] == -1:
            last_dict['isChinese'] = this_dict['isChinese']
        if this_dict['isChinese'] != last_dict['isChinese']:
            rtn_str += str_o[record_ind:this_dict['ptr']] + ' '
            record_ind = this_dict['ptr']
        # Move forward one step
        last_dict['isChinese'] = this_dict['isChinese']
        last_dict['ptr'] = this_dict['ptr']
        this_dict['ptr'] += 1
    rtn_str += str_o[record_ind:]
    return rtn_str


def digit_seperate(str_o):
    rtn_str = ''
    last_is_digit = False
    for c in str_o:
        if c in '0123456789':
            if not last_is_digit:
                # From non-digit to digit --> switch
                rtn_str = rtn_str + ' %s' % c
                last_is_digit = True
            else:
                # From digit to digit --> pass
                rtn_str += c
        else:
            if last_is_digit:
                # From digit to non-digit --> switch
                rtn_str = rtn_str + ' %s' % c
                last_is_digit = False
            else:
                # From digit to digit --> pass
                rtn_str += c
    return rtn_str


def guess_language(str_txt):
    in_zh_set = False
    for c in str_txt:
        if (c >= u'\u4e00' and c <= u'\u9fa5'):
            in_zh_set = True
        if (c >= u'\u3040' and c <= u'\u31ff'):
            return 'ja'
    if in_zh_set:
        return 'zh'
    else:
        return 'UNKOWN'


# Clear Index for Re-index
def get_clear_index_dict(search_obj, userID):
    check_list = INDEX_LIST
    rtn_dict = {}
    rtn_dict['django_ct'] = '%s.%s' % (search_obj.app_label, search_obj.model_name)
    rtn_dict['django_id'] = search_obj.pk
    if userID == 'site':
        rtn_dict['id'] = '%s.%s' % (rtn_dict['django_ct'], search_obj.pk)
    else:
        rtn_dict['id'] = '%s.%s_%s' % (rtn_dict['django_ct'], search_obj.pk, userID)
    # rtn_dict['owner'] = '%s'% userID
    for field in check_list:
        if field in search_obj.__dict__:
            rtn_dict[field] = search_obj.__dict__[field]
    return rtn_dict


def clear_dict(index_dict, userID):
    check_list = INDEX_LIST
    rtn_dict = {}
    rtn_dict['django_ct'] = index_dict['django_ct']
    rtn_dict['django_id'] = index_dict['django_id']
    if userID == 'site':
        rtn_dict['id'] = '%s.%s' % (rtn_dict['django_ct'], rtn_dict['django_id'])
    else:
        rtn_dict['id'] = '%s.%s_%s' % (rtn_dict['django_ct'], rtn_dict['django_id'], userID)
    # rtn_dict['owner'] = '%s'% userID
    for field in check_list:
        if field in index_dict:
            rtn_dict[field] = index_dict[field]
    return rtn_dict


def prepare_nickname_index(index, nickname):
    index['nickname'] = nickname
    index['text'] = '%s %s' % (index['name'], index['nickname'])
    return index


# Increase score of specific user for index dictionary
def increase_score(index_dict, score):
    # Update from original Index
    field_name = 'rank_score'
    if field_name in index_dict:
        index_dict[field_name] += score
    else:
        index_dict[field_name] = score
    return index_dict


# === Todo: Write Test ===
# Open Usage Function
def personal_ranking(s_qs, user):
    """
       Get personal ranking for any haystack query set.

    s_qs: SearchQuerySet of haystack
    user: User OBJ. The one who wants to get personal ranking results
    """
    return s_qs
    # return s_qs.order_by('-rank_score').filter(owner__in=['%s'%user.id,'site'])


# === Todo: Modify Test ===
def global_ranking(s_qs):
    """
       Exclude all replica (personal) indexes for a haystack query set.
       Get global ranking for search.

    s_qs: SearchQuerySet of haystack
    """
    # return s_qs.filter(owner='site')
    return s_qs


# === Todo: Write Test ===
def get_clear_search_results(search_results):
    """
       Remove all replica (personal) objects for haystack query results.

    search_results: SearchResult of haystack
    """
    unique_set = set()
    clear_search_results = []
    for result in search_results:
        if not result:
            pass
        else:
            if result.pk not in unique_set:
                clear_search_results.append(result)
                unique_set.add(result.pk)
            else:
                pass
    return clear_search_results


# === Todo: Write Test ===
def spatial_ranking(s_qs, latitude, longitude, dist=INIT_SEARCH_DELTA, pure_dist=False):
    """
       Get Spatial Search.

    s_qs: SearchQuerySet of haystack
    latitude, longitude: Location of user
    """
    # Point(longitude, latitude)
    query_pt = Point(longitude, latitude)
    # Within a two miles.
    max_dist = D(km=dist)

    # Do the radius query.
    if pure_dist:
        return s_qs.dwithin('latlon', query_pt, max_dist).distance('latlon', query_pt).order_by('distance')
    else:
        return s_qs.dwithin('latlon', query_pt, max_dist)

