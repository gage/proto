from django.http import HttpResponse
from django.utils import simplejson

def HttpJsonResponse(data={}, ensure_ascii=False, mimetype="application/json", success=True):
    if not success:
        data['status'] = 0
        if 'msg' not in data.keys():
            data['msg'] = 'request error.'
    else:
        data['status'] = 1
    return HttpResponse(simplejson.dumps(data, ensure_ascii=ensure_ascii), mimetype=mimetype)