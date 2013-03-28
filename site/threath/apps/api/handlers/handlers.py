import json

from haystack.query import SearchQuerySet, SQ
from piston.handler import BaseHandler as PistonHandler

from search.utils import process_query, spatial_ranking, get_clear_search_results
from api.utils import process_latlon, process_integer

# ============== Operation Handler =============
class BaseHandler(PistonHandler):
    """This handler is s a base handler.
    """
    # Allowed request methods: might be 'POST', 'GET', 'DELETE'
    allowed_methods = ('POST', )

    # For POST:
    # required_fields - lists the parameters that must be specified
    # create_kwargs - only the parameters in create_kwargs will be kept. (it is a superset of required_fields)
    # files_kwargs - corresponding to request.FILES
    # form_fields - only the parameters in form_fields will be updated. (for update object)
    # perform_save - perform save operation for object update. it might cause risk condition if it is set as "True".
    #                True -> update, False -> save
    required_fields = ()
    create_kwargs = ()
    files_kwargs = ()
    form_fields = ()
    update_instead_save = False

    # For GET:
    # required_fields_for_read - lists the parameters that must be specified for read 
    # read_kwargs - only the parameters in read_kwargs will be kept.
    # allowed_filter - only the parameters in allowed_filter will be used as query params.
    # filter_opt - define several type of special query (see: notify/handlers.py).
    # para_mapping - used for mapping the read_kwargs to allowed_filter
    required_fields_for_read=()
    read_kwargs = ()
    allowed_filter = ()
    filter_opt = ()
    para_mapping = {}

    # For DELETE:
    # delete_kwargs - lists the parameters that must be specified
    delete_kwargs = ()


    # Settings:
    # query_model - model to query
    # about_privacy - if about_privacy is True, then use "viewables" to query object
    # default_order - the default sorting order, which might be "-timestamp", "updated" and so on.
    # read_auth_exempt - if this parameter is True, then the GET request of this resource is authenticatation exempt
    # create_auth_exempt - if this parameter is True, then the POST request of this resource is authenticatation exempt
    query_model = None
    about_privacy = False
    default_order = None
    read_auth_exempt = False
    create_auth_exempt = False

    def __init__(self):
        if not self.create_kwargs:
            self.create_kwargs = self.required_fields

    def auth_resource(self, request, json_dict, **kwargs):
        # We should implement GET, POST, DELETE authentication here.
        return

    def map_para(self, query_dict):
        # Automatically strip Id from the end of input key
        for key in query_dict.keys():
            if key in self.para_mapping.keys():
                mapped_key = self.para_mapping[key]
                query_dict[mapped_key] = query_dict[key]
            elif key.endswith('_id'):
                mapped_key = key[:-3]
                query_dict[mapped_key] = query_dict[key]
        return query_dict

    def create_validate(self, query_dict, **kwargs):
        pass

    def read_validate(self, query_dict, **kwargs):
        pass

    def delete_validate(self, query_dict, **kwargs):
        pass

# ============== Index Handler =============
class BaseIndexHandler(BaseHandler):
    """
    This handler is used to manager the url like :collection/
    It allows POST and GET method.
    We can use GET method to query objects in :collection
    and use POST to create an object belongs to this :collection
    """
    allowed_methods = ('POST', 'GET')

    def read(self, request, **kwargs):
        """ Query """
        offset = request.CLEANED['offset']
        endpoint = request.CLEANED['endpoint']

        if 'custom_query' in request.CLEANED:
            query_set = request.CLEANED['custom_query']
        elif self.about_privacy:
            query_set = self.query_model.viewables(user=request.user)
        else:
            query_set = self.query_model.objects.all()

        # query_list = []
        query_args = {}

        if not 'use_custom_only' in request.CLEANED:
            for key, value in request.CLEANED.iteritems():
                if key in self.allowed_filter:
                    if isinstance(value, basestring) and ',' in value:
                        query_args[key + '__in'] = value.split(',')
                    else:
                        query_args[key] = value

        results = query_set.filter(**query_args)
        if request.CLEANED['order_by']:
            results = results.order_by(request.CLEANED['order_by'])
        elif self.default_order:
            results = results.order_by(self.default_order)

        fields = {k: request.CLEANED[k] for k in ('detail', 'to_card', 'create_card')}

        if kwargs.get('all') and kwargs.get('raw'):
            return [r for r in results]
        if kwargs.get('all'):
            return [r.to_json(request=request, **fields) for r in results]
        if kwargs.get('raw'):
            return [r for r in results[offset:endpoint]]
        return [r.to_json(request=request, **fields) for r in results[offset:endpoint]]


# ============== Object Handler =============
class BaseObjectHandler(BaseHandler):
    """
    This handler is used to manage the url like :collection/:object_id
    It allows POST, GET and DELETE method.
    We can use GET method to get object of :collection/:object_id
    and use POST to update the object -- or doing some specific operation.
    Use DELETE to delete the object.
    """
    allowed_methods = ('POST', 'GET', 'DELETE')
    form_fields = ()
    update_instead_save = False

    def read(self, request, object_id, **kwargs):
        if request.CLEANED.get('_obj'):
            result = request.CLEANED.get('_obj')
        else:
            result = self.query_model.objects.get(id=object_id)

        fields = {k: request.CLEANED[k] for k in ('detail', 'to_card', 'create_card')}
        return result.to_json(request=request, **fields)

    def delete(self, request, object_id, **kwargs):
        if request.CLEANED.get('_obj'):
            result = request.CLEANED.get('_obj')
        else:
            result = self.query_model.objects.get(id=object_id)
        result.delete()
        return

    def create(self, request, object_id, **kwargs):
        changed_fields = {}
        if request.CLEANED.get('_obj'):
            result = request.CLEANED.get('_obj')
        else:
            result = self.query_model.objects.get(id=object_id)
        for key, value in request.CLEANED.iteritems():
            if value != None and key in self.form_fields:
                setattr(result, key, value)
                changed_fields[key] = value
        if changed_fields:
            if self.update_instead_save:
                self.query_model.objects.filter(id=object_id).update(**changed_fields)
            else:
                result.save()
        # return ','.join(changed_fields)
        fields = {k: request.CLEANED[k] for k in ('detail', 'to_card', 'create_card')}
        fields['detail'] = True
        return result.to_json(request=request, **fields)


# ============== Search Handler =============
class BaseSearchHandler(BaseHandler):
    """
    This handler is used to search objects
    """
    allowed_methods = ('GET', )
    read_kwargs = ('filter_type', 'q', 'location', 'distance', 'search_fields', )
    allowed_filter = ('text', )
    # Default is auto_query
    filter_opt = ('auto_query', 'startswith', 'location', 'auto_complete')

    def read_validate(self, query_dict, **kwargs):
        process_integer(query_dict, ['distance'])
        if query_dict.get('distance')==None:
            # Default 100km
            query_dict['distance'] = 100

        if not query_dict.get('filter_type'):
            query_dict['filter_type'] = 'auto_query'
        elif query_dict['filter_type'] == 'location':
            query_dict['location'] = process_latlon(query_dict.get('location'))

        if not query_dict.has_key('q'):
            query_dict['q'] = ''
        if not query_dict.has_key('search_fields'):
            query_dict['search_fields'] = self.allowed_filter
        else:
            query_dict['search_fields'] = filter(lambda x: x in self.allowed_filter, query_dict['search_fields'].split(','))

    def read(self, request):
        """ Search """
        query_term = request.CLEANED['q']
        filter_type = request.CLEANED['filter_type']
        search_fields = request.CLEANED['search_fields']
        offset = int(request.CLEANED['offset']) if request.CLEANED['offset'] else None
        endpoint = int(request.CLEANED['endpoint']) if request.CLEANED['offset'] else None
        total_count = request.CLEANED['total_count'] == True if 'total_count' in request.CLEANED else False
        if not request.CLEANED.has_key('distance'):
            raise Exception('Call super read_validate when overwrite')
        distance = request.CLEANED['distance']
        if request.CLEANED.has_key('custom_query'):
            query_set = request.CLEANED['custom_query']
        else:
            if type(self.query_model)==list:
                query_set = SearchQuerySet().models(*self.query_model).load_all()
            else:
                query_set = SearchQuerySet().models(self.query_model).load_all()

        if self.about_privacy:
            # TODO
            pass

        query_list = []
        query_args = {}
        if filter_type == 'auto_query':
            query_set = query_set.auto_query(query_term)

        elif filter_type == 'auto_complete':
            query_set = query_set.filter(SQ(auto_complete=query_term))

        elif filter_type == 'startswith' or filter_type == 'location':
            query_term_list = process_query(query_term)
            for term in query_term_list:
                query_list.append(reduce(lambda a, b: a | b, [SQ(**{field + '__startswith':term}) for field in search_fields] + [SQ(**{field:term}) for field in search_fields]))
        if filter_type == 'location':
            latitude, longitude = request.CLEANED['location']
            query_set = spatial_ranking(query_set, latitude, longitude, distance, pure_dist=True)

        results = query_set.filter(*query_list)
        if total_count:
            return (results._clone().count(), get_clear_search_results(results[offset:endpoint]))
        else:
            return get_clear_search_results(results[offset:endpoint])



# ============== Attribute Handler =============
class BaseAttributeHandler(BaseHandler):
    """
    This handler is used to manager the url like :collection/:object_id/:attribute
    It allows POST, GET and DELETE method.

    The attribute should be a ListField or SetField with IDs.

    We can use GET method to get objects for :collection/:object_id/:attribute
    and use POST to add an item from the attibute.
    Use DELETE to remove an item from the attibute.
    """
    allowed_methods = ('POST', 'GET', 'DELETE')
    required_fields = ('attr_value', )
    delete_kwargs = required_fields
    field_model = None

    def validate(self, query_dict, object_id, **kwargs):
        query_dict['target'] = self.query_model.objects.get(id=object_id)

    read_validate = validate
    create_validate = validate
    delete_validate = validate

    def read(self, request, object_id, attr):
        values = getattr(request.CLEANED['target'], attr)
        if not self.field_model:
            return list(values)
        offset = request.CLEANED['offset']
        endpoint = request.CLEANED['endpoint']
        results = self.field_model.objects.filter(id__in=values)
        fields = {k: request.CLEANED[k] for k in ('detail', 'to_card', 'create_card')}        
        return [r.to_json(request=request, **fields) for r in results[offset:endpoint]]

    def delete(self, request, object_id, attr):
        raise NotImplementedError("Implement delete method.")

    def create(self, request, object_id, attr):
        raise NotImplementedError("Implement create method.")



