import time, Queue
import haystack
import datetime
from globals.threads import GeneralThread
from django.contrib.auth.models import User
from search.utils import handle_action_for_ranking, get_clear_index_dict, prepare_nickname_index
from haystack.query import SearchQuerySet


class HandleActionScoreThread(GeneralThread):
    MAX_NUM = 1
    thread_num = 0    
    Pool = Queue.Queue( 0 )
    
    def run(self):
        while True:          
            action = self.Pool.get()
            try:
                handle_action_for_ranking(action)
            except Exception, e:
                print 'Fail on action scoring.'
                print e
            self.Pool.task_done()


class UpdateNicknameThread(GeneralThread):
    MAX_NUM = 1
    thread_num = 0    
    Pool = Queue.Queue( 0 )
    
    def run(self):
        rtn_dict_list = []
        start_time = datetime.datetime.now()
        while True:
            contact = self.Pool.get()
            if contact != None:
                if datetime.datetime.now() - contact.created < datetime.timedelta(seconds=5):
                    time.sleep(5)
                target = contact.site_user
                owner = contact.user
                nickname = contact.get_name()
                search_qs =  SearchQuerySet().models(User)\
                    .filter(owner=owner.id).filter(django_id=target.id)
                if not search_qs:
                    # This is for Object Creation. When we create an object, it may 
                    # not be indexed yet so we cannot get results and have to wait a sec.
                    time.sleep(1)
                    search_qs = SearchQuerySet().models(User)\
                        .filter(owner=owner.id).filter(django_id=target.id)
                if search_qs:
                    search_obj = search_qs[0]
                    index = get_clear_index_dict(search_obj, owner.id)
                    index = prepare_nickname_index(index, nickname) 
                    rtn_dict_list.append(index)                    
                else:
                    pass

            self.Pool.task_done()
                
            if len(rtn_dict_list) > 500 or datetime.datetime.now() - start_time > datetime.timedelta(seconds=5) or self.Pool.qsize() < 2:
                # Do index and Reset                
                haystack.backend.SearchBackend().update_with_dict(index_dict_list=rtn_dict_list)
                print 'Build index for:', contact
                rtn_dict_list = []
                start_time = datetime.datetime.now()
