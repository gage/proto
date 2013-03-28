import threading

from django.contrib.auth.models import User
# from file_sharing.models import ShareFile, Folder
# from place_book.models import PlaceBook, PlaceCard
# from contact_book.models import ContactBook, ContactCard
# from wantto.models import WantTo
from globals.utils import get_index, get_search_backend


class RebuildModelThread(threading.Thread):

    def __init__(self, model):
        self.model = model
        threading.Thread.__init__(self)

    def run(self):
        model = self.model
        if model == 'user':
            get_search_backend().remove_by_query(query='django_ct:auth.user')
            search_index = get_index(User)
            get_search_backend().update(index=search_index, iterable=User.objects.all(), commit=True)
        # elif model == 'file':
        #     get_search_backend().remove_by_query(query='django_ct:file_sharing.sharefile')
        #     search_index = get_index(ShareFile)
        #     get_search_backend().update(index=search_index, iterable=ShareFile.objects.all(), commit=True)
        # elif model == 'folder':
        #     get_search_backend().remove_by_query(query='django_ct:file_sharing.folder')
        #     search_index = get_index(Folder)
        #     get_search_backend().update(index=search_index, iterable=Folder.objects.all(), commit=True)
        # elif model == 'place_book':
        #     # Place Book
        #     get_search_backend().remove_by_query(query='django_ct:place_book.placebook')
        #     search_index = get_index(PlaceBook)
        #     get_search_backend().update(index=search_index, iterable=PlaceBook.objects.all(), commit=True)
        #     # Place Card
        #     get_search_backend().remove_by_query(query='django_ct:place_book.placecard')
        #     search_index = get_index(PlaceCard)
        #     get_search_backend().update(index=search_index, iterable=PlaceCard.objects.all(), commit=True)
        # elif model == 'wantto':
        #     get_search_backend().remove_by_query(query='django_ct:wantto.wantto')
        #     search_index = get_index(WantTo)
        #     get_search_backend().update(index=search_index, iterable=WantTo.objects.all(), commit=True)
        # elif model == 'contact_book':
        #     # Contact Book
        #     get_search_backend().remove_by_query(query='django_ct:contact_book.contactbook')
        #     search_index = get_index(ContactBook)
        #     get_search_backend().update(index=search_index, iterable=ContactBook.objects.all(), commit=True)
        #     # Contact Card
        #     get_search_backend().remove_by_query(query='django_ct:contact_book.contactcard')
        #     search_index = get_index(ContactCard)
        #     get_search_backend().update(index=search_index, iterable=ContactCard.objects.all(), commit=True)
        else:
            return 'Wrong model=...%s' % model
