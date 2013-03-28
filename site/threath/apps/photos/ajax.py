""" Site photos module AJAX views """
from django.contrib.auth.models import User

import os
import json
import time
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from actstream.models import Action
#from actstream.specs import ActstreamSpecs
from videostream.models import VideoStream
from photos.models import Photo
from place.models import Place
from review.models import Review
from events.models import Event
from globals.utils import gen_a_post, total_milliseconds

TYPE_FALLBACK_PLACE = "place"
TYPE_FALLBACK_DISH = "dish"
TYPE_FALLBACK_USER = "user"


class PhotoDetailType:
    '''
    The type definition for photo detail 
    '''
    PLACE_PHOTO = "place_photo"
    PLACE_REVIEW = "place_review"
    DISH_REVIEW = "dish_review"
    USER_PHOTO = "user_photo"
    EVENT_PHOTO = "event_photo"

def get_photo_detail( request, object_id=None, photo_id=None, event_id=None, photo_detail_type=None, is_render_to_string=False ):
    # time_start = datetime.now()
    
    ct_event = ContentType.objects.get_for_model(Event)
    ct_review = ContentType.objects.get_for_model(Review)
    user = request.user
    
    if not photo_id or not photo_detail_type:
        photo_id = request.POST['photo_id']
        photo_detail_type = request.POST['photo_detail_type']
    
    #from view
    if event_id:
        # only place and user profile have event photos
        object_id = event_id
    else:
        # from view
        if object_id:
            pass
        # from ajax
        else: 
            object_id = request.POST.get('object_id', None)
    
    photo = Photo.objects.get(pk=photo_id)
    photo_owner = photo.user
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)
    # print "Stage 0.5: %d" % time_elapsed

    # if not p_photo.viewable_by(user):
    #     raise Exception("You don't have permission to see this photo.")
    #     if is_render_to_string:
    #         raise Exception("You don't have permission to see this photo.")
    #     else:
    #         raise Exception("You don't have permission to see this photo.")
    # 
    # if user.is_anonymous():
    #     raise Exception('you are not a site user')
    
    # time_start = time_end
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)    
    # print "Stage 1: %d" % time_elapsed
    
    #===========================================================================
    # special case for the view of event photo detail page 
    #===========================================================================
    if photo.content_type == ct_event:
        photo_detail_type = PhotoDetailType.EVENT_PHOTO
        object_id = photo.object_id
        url_4_html5 = reverse('event-photo-detail', args=[object_id, photo.id])
         
    if photo_detail_type == PhotoDetailType.PLACE_PHOTO:
        photos = Photo.viewables(user).filter( place=photo.place.id ).exclude(content_type=ct_event).order_by('-created')
        url_4_html5 = reverse('place-photo-detail', args=[photo.place.id, photo.id]).replace('None', '')
    
    elif photo_detail_type == PhotoDetailType.PLACE_REVIEW:
        photos = Photo.viewables(user).filter( place=photo.place.id, content_type=ct_review ).order_by('-created')
        url_4_html5 = reverse('place-review-detail', args=[photo.place.id, photo.id])
    
    elif photo_detail_type == PhotoDetailType.DISH_REVIEW:
        photos = Photo.viewables(user).filter( dish=photo.dish.id, content_type=ct_review ).order_by('-created')
        url_4_html5 = reverse('dish-review-detail', args=[photo.dish.id, photo.id])
    
    elif photo_detail_type == PhotoDetailType.USER_PHOTO:
        photos = Photo.viewables(user).filter( user=photo_owner, content_type=ct_review).order_by('-created')
        url_4_html5 = reverse('userprofile-photo-detail', args=[photo_owner.id, photo.id]).replace('None', '')
    
    elif photo_detail_type == PhotoDetailType.EVENT_PHOTO:
        event = Event.objects.get(pk=object_id)
        photos = Photo.viewables(user).filter(object_id=event.id).order_by('-created')
        url_4_html5 = reverse('userprofile-photo-detail', args=[photo_owner.id, photo.id])
    else:
        raise Http404
    
#    print "photo_detail_type: %s" % photo_detail_type
    
    
    #===========================================================================
    # keep photo sequence into session 
    #===========================================================================
    
    #ppdl is acronym of Privacy Photo Detail List 
    ppdl = request.session.get('ppdl', [] )
    
    def create_session():
        request.session['ppdl'] = list(photos)
        request.session['ppdl_created'] = datetime.utcnow()  
        request.session['ppdl_type'] = photo_detail_type
        
    # time_start = time_end        
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)    
    # print "Stage 2: %d" % time_elapsed
    # save ppdl in session at the first time user access a detail page
    if not ppdl:
        create_session()
    else:
        # ppdl = request.session['ppdl']
        ppdl_created = request.session['ppdl_created']
        ppdl_type = request.session['ppdl_type']
        elapsed_time = datetime.utcnow() - ppdl_created
        
        #======================================================================
        # modify session if 
        # photo detail type is not the same as the last time user access
        # or
        # the ppdl session has expired (life cycle: 30 mins)
        #======================================================================
        if ppdl_type != photo_detail_type or elapsed_time.seconds > 30*60:
#            print "modify session: case I"
            create_session()
        # modify session if p_photos has been changed
        elif len(ppdl) != photos.count():
#            print "modify session: case II"
            create_session()
        # modify session due to some cases of event photo
        else:
            if photo not in ppdl:
                create_session()
#                print "modify session: case III"
            else:
#                print "access session"
                pass
            
    ppdl = request.session['ppdl']
    # time_start = time_end        
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)    
    # print "Stage 2.5: %d" % time_elapsed
    
    total = len(ppdl)


    #===========================================================================
    # handle photo display sequence
    #===========================================================================
    try:
        cur_index = ppdl.index( photo )
    except ValueError:
        raise Exception("ppdl:%s\nphotos:%s\nphoto.id:%s" % (ppdl, photos, photo.id) )
    
        
    next_index = cur_index + 1
    pre_index = cur_index -1
    
    if cur_index == 0:
        pre_index = total - 1
        
    if cur_index == total - 1:
        next_index = 0
    
    review = None
    event = None
    # time_start = time_end        
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)    
    # print "Stage 2.75: %d" % time_elapsed
    if photo.get_review() != None:
        review = photo.content_object

    elif photo.get_event() != None:
        event = photo.content_object
        
    # time_start = time_end        
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)    
    # print "Stage 3: %d" % time_elapsed
    
    #===========================================================================
    # organize photo preloading list
    #===========================================================================
    def get_preloaded_list( index, photo_list ):
        num_pre_item = 3
        num_post_item = 8
        preload_list = []
        p_pre = index - num_pre_item
        p_post = index + num_post_item 
        
        if p_pre < 0:
            preload_list.extend(photo_list[0:index])
            preload_list.extend(photo_list[p_pre:])
        else:
            preload_list.extend(photo_list[p_pre:index])
        
        if p_post > total - 1:
            preload_list.extend(photo_list[index+1:])
            preload_list.extend(photo_list[:p_post - (total-1)])
        else:
            preload_list.extend(photo_list[index+1:p_post])
        
        return set(preload_list)    
    
    preload_list = get_preloaded_list(cur_index, ppdl)
    
    # time_start = time_end        
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)    
    # print "Stage 4: %d" % time_elapsed
    
    #===========================================================================
    # arrange the parameters required by the inc_post_boilerplate.html
    #===========================================================================
    allow_comment="1"
    action = None
    if review:
        avatar = review.user.get_profile()
        user_profile = avatar.get_profile()
        
        if not user_profile.public_comments or avatar.not_visible_by(request.user):
            allow_comment="0"
        
        content = review.content
        post_time = review.created
        comment_target = review
        
        if review.dish:
            pre_content_object = review.dish
            post_content_object = review.place
            todo_target = review.dish
        else:
            pre_content_object = review.place
            post_content_object = None
            todo_target = review.place
        
#        try:
#            action = Action.objects.get(target_object_id = review.id, verb = ActstreamSpecs.POSTED_A_REVIEW)
#        except ObjectDoesNotExist:
#            action = None
            
    elif event:
        avatar = photo.user.get_profile()
        user_profile = avatar.get_profile()
 
        if not user_profile.public_comments or avatar.not_visible_by(request.user):
            allow_comment="0"
 
        content = photo.description
        post_time = photo.created
        comment_target = photo
        
        if photo.dish:
            pre_content_object = photo.dish
            post_content_object = photo.place
            todo_target = photo.dish
        else:
            pre_content_object = photo.place
            post_content_object = None
            todo_target = photo.place
    # mturk photo
    else:
        if photo.place:
            avatar = photo.place
            pre_content_object = photo.place
            post_content_object = None
            todo_target = photo.place
        else:
            avatar = None
            pre_content_object = None
            post_content_object = None
            todo_target = None
        
        user_profile = None
        content = "Photo from: %s" % photo.urlOwner
        post_time = photo.created
        comment_target = photo
        
    target_content_type_id = ContentType.objects.get_for_model(comment_target).id
    
    # time_start = time_end        
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)    
    # print "Stage 5: %d" % time_elapsed
    
    pps = gen_a_post(
        allow_comment=allow_comment,
        avatar=avatar,
        user_profile=user_profile,
        pre_content_object=pre_content_object,
        post_content_object=post_content_object,
        content=content,
        post_time=post_time,
        todo_target=todo_target,
        target_content_type_id=target_content_type_id,
        comment_target=comment_target,
        request=request,
        action = action,
    )
    print "url_4_html5", url_4_html5
    
    # time_start = time_end        
    # time_end = datetime.now()
    # time_elapsed = total_milliseconds(time_end - time_start)    
    # print "Stage 6: %d" % time_elapsed
    
    context={
        "review": review,
        "photo": photo,
        "preload_list": preload_list,
        "next_pid": ppdl[next_index].id,
        "pre_pid": ppdl[pre_index].id,
        "pps": pps,
        "object_id": object_id,
        "url_4_html5": url_4_html5
    }
    
    if is_render_to_string:
        rtn = render_to_string( 'inc_photos_details.html',
                                  context,
                                  context_instance = RequestContext(request)
                                  )
        return rtn
    else:
        # time_start = time_end        
        # time_end = datetime.now()
        # time_elapsed = total_milliseconds(time_end - time_start)    
        # print "Stage 7: %d" % time_elapsed 
        rtn = render_to_response( 'inc_photos_details.html',
                                   context,
                                   context_instance = RequestContext(request)
                                   )        
        # time_start = time_end        
        # time_end = datetime.now()
        # time_elapsed = total_milliseconds(time_end - time_start)    
        # print "Stage 8: %d" % time_elapsed
        return rtn

def get_fallback_photo(request, type, width, height):
    if type == TYPE_FALLBACK_PLACE:
        default_photo = Photo.objects.filter( place_default=True )[0]
    elif type == TYPE_FALLBACK_DISH:
        default_photo = Photo.objects.filter( dish_default=True )[0]    
    elif type == TYPE_FALLBACK_USER:
        default_photo = Photo.objects.filter( user_default=True )[0]
    else:
        return HttpResponseBadRequest("invalid type!")
    
    size_str = 'image%sx%s' % (width, height)
    default_photo = getattr(default_photo, size_str)

    return HttpResponse( default_photo.url )

def upload_photo(request):
    """ Remotely uploads a photo and returns a JSON TempPhoto object

    GET Parameters:
        qqfile:     Name of the file being uploaded, if the browser supports XHR
                    uploads this will apear in request.raw_post_data
        spec:       Name of the ImageSpec to proess this photo with.  Make sure
                    the ImageSpec actually exists in photos.imagespecs otherwise
                    bad things will happen.

    Returns:
        {
            'status':   1 if successful, 0 otherwise
            'id':       ID of the newly created TempPhoto object,
            'url':      URL to display the imagespec-processed photo requested,
            'message':  Error message, only if status==0,
        }
    """
    
    
    #Browser detection
    browser = None
    if 'MSIE' in request.META['HTTP_USER_AGENT']:
        browser = 'ie'
    elif 'Firefox/3.0' in request.META['HTTP_USER_AGENT']:
        browser = 'ff3'
    
    if browser in ['ff3', 'ie']:
        mimetype="text/html"
    else:
        mimetype="application/json"
    
    if request.method == 'POST':
        
        if browser in ['ff3', 'ie']:
            filename = request.FILES['qqfile']._name
        else:
            filename = request.GET.get('qqfile', None)
        
        if filename:
            # TODO: SimpleUploadedFile is the in-memory upload handler.  Is this
            # going to kill our server with large files?
            if browser in ['ff3', 'ie']:
                file = request.FILES['qqfile']
            else:
                file = SimpleUploadedFile(filename, request.raw_post_data)
                
            user_id = request.POST.get('user_id', None)
            user = request.user
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    response = {
                        'status': 0,
                        'message': "User does not exit: %s" % user_id,
                    }
                    return HttpResponse(json.dumps(response), mimetype=mimetype)
            
            user_id = user.id
            if user.is_anonymous():
                user = None
                user_id = 'site'
            
            chunk = filename.split('.')
            extension = ''
            if len(chunk) > 1:
                extension = chunk[len(chunk)-1]
            extension = extension.lower()
            
            if extension not in ['mp4', 'jpg', 'gif', 'png', 'jpeg']:
                response = {
                    'status': 0,
                    'message': "Extension error!",
                }
                return HttpResponse(json.dumps(response), mimetype=mimetype)
            
            if extension == 'mp4':
                video = VideoStream.objects.create(videoupload=file, user=user)
                response = {
                    'status': 1,
                    'id': video.id,
                    'url': video.get_absolute_url(),
                    'type': 'video',
                }
            else:
                if settings.DEFAULT_FILE_STORAGE == "storages.backends.s3boto.S3BotoStorage":
                    # Now we adapt to s3 storage so need directly use rawdata                
                    photo = Photo(image=file, user=user)                
                    
                else:
                    # Origin method: only can work with local disk,
                    relative_path = "photos/%s_%s_%s" % (user_id, int(time.time()), filename)
                    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                    # Write the file to disk
                    destination = open(full_path, 'wb+')
                    for chunk in file.chunks():
                        destination.write(chunk)
                    destination.close()
                    # Create the photo object
                    photo = Photo(image=relative_path, user=user)
                    
                    
                photo.save()
                # Photo.objects.filter(pk=photo.pk).update(user=user.id)
    
                # Try to use the spec provided
                spec = request.GET.get('spec', None)
                if not spec:
                    response = {
                        'status': 0,
                        'message': "No imagespec specified.",
                    }
                    return HttpResponse(json.dumps(response), mimetype=mimetype)
                if not hasattr(photo, spec):
                    response = {
                        'status': 0,
                        'message': "Imagespec %s does not exist." % spec,
                    }
                    return HttpResponse(json.dumps(response), mimetype=mimetype)
    
                type = request.GET.get('type', None)
                id = request.GET.get('id', None)
                if type == 'event' and id:
                    from events.models import Event
                    try:
                        event = Event.objects.get(id=id)
                        photo.attach(event)
                        photo.event = event
                        event.add_photo(photo)
                    except Event.DoesNotExist:
                        raise Http404
                response = {
                    'status': 1,
                    'id': photo.id,
                    'url': getattr(photo, spec).url,
                    'type': 'photo',
                }
        else:
            response = {
                'status': 0,
                'message': "No file could be found.",
            }
    else:
        response = {
            'status': 0,
            'message': "No file uploaded.  Please try again.",
        }
    return HttpResponse(json.dumps(response), mimetype=mimetype)
