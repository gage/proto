""" UserProfile's utils """

__author__ = "Sean Cheng <sean.cheng@geniecapital.com.tw>"

from contact.models import SOCIAL_FACEBOOK, SOCIAL_MIXI, SOCIAL_WEIBO
from facebook.facebook_api import FacebookAPI
from mixi.models import MixiProfile
from weibo.models import WeiboProfile

SOCIAL_DICTS = {
    SOCIAL_FACEBOOK: FacebookAPI,
    SOCIAL_MIXI: MixiProfile,
    SOCIAL_WEIBO: WeiboProfile
}

PUSH_VERB_LIST = ['post on wall', 'wants to']


def update_site_user_info(user):
    raise Exception("This method is deprecated temporary. Please consult Sean first if you wanna use it anyway.")

    """
    When a new site user created in example.com, we use post save signal to trigger this function.
    Update existing data, including:
    0. Social Network Importing
    1. Public page comment
    2. Event and Invitation
    3. Others' Contact
    4. Post tags
    (In Future)
    5. Public and Event photo
    6. Notification and Action
    """
    from django.contrib.comments.models import Comment
    from actstream.models import Action
    from events.models import Invitation, Event
    from contact.models import Contact
    from contact.importer import BuildContactThread
    # from wantto.models import WantTo
    from post.models import Post
    user_profile = user.get_profile()
    email = user.email

    if not email:
        return

    # Process 1. Public page comment
    Comment.objects.filter(user_email=email).update(user=user)
    # Process 2. Event and Invitation
    for invitation in Invitation.objects.filter(email=email):
        # Update event and chat infomation
        event = invitation.event
        event.chat.join_chat_by_user(user)
        event.site_user_set.add(user.id)
        event.save()
        # Update invitation into site_user
        invitation.recipient = None
        invitation.site_user = user
        # Update session and inv_id
        invitation.inv_id = None
        invitation.session_uuid = user_profile.get_uuid()
        invitation.save()
    # Process 3. Others' Contact
    # Here we don't use update because the save function help us do several checking and solr indexes.
    for contact in Contact.objects.filter(email=email, site_user__isnull=True):
        contact.site_user = user
        contact.save()

    # Split Slave contact when correspond to a site_user
    for contact in Contact.objects.all_filter(email=email, is_slave=True):
        contact.release_from_master(commit=False)
        contact.site_user = user
        contact.save()

    # Process 4. Post tags
    for post in Post.objects.filter(tagged_email=email):
        post.tagged_people.add(user.id)
        try:
            post.tagged_email.remove(email)
        except KeyError:
            pass
        post.save()
        actions = Action.objects.filter(target_object_id=post.id, verb__in=PUSH_VERB_LIST)
        for action in actions:
            action.push_to.add(user.id)
            action.save()

    for wt in WantTo.objects.filter(tagged_emails=email):
        wt.tagged_users.add(user.id)
        try:
            wt.tagged_emails.remove(email)
        except KeyError:
            pass
        wt.save()
        actions = Action.objects.filter(target_object_id=wt.id, verb__in=PUSH_VERB_LIST)
        for action in actions:
            action.push_to.add(user.id)
            action.save()


def migrate_user_info(master, slave):
    # Slave --> Master
    from django.contrib.comments.models import Comment
    from actstream.models import Action
    from events.models import Invitation, Event
    from contact.models import Contact
    from dare.models import Dare
    from dish.models import Dish
    from events.models import Event, Invitation
    from facebook.models import FacebookProfile
    from like.models import LikableModel
    # from notify.models import Notify
    from photos.models import Photo
    # from post.models import Post
    from privacy.models import PrivacyRespectingModel
    from todo.models import TodoItem
    # from wantto.models import WantTo
    from videostream.models import VideoStream

    # Event and Invitation
    for invitation in Invitation.objects.filter(email=slave.email):
        # Update event and chat infomation
        event = invitation.event
        if master.id not in event.site_user_set:
            event.chat.join_chat_by_user(master)
            event.site_user_set.add(master.id)
            # Update invitation into site_user
            invitation.recipient = None
            invitation.site_user = master
            # Update session and inv_id
            invitation.inv_id = None
            invitation.session_uuid = master.get_profile().get_uuid()
            invitation.save()
        else:
            invitation.delete()
        if slave.id in event.site_user_set:
            event.site_user_set.remove(slave.id)
        event.save()

    # Models
    Action.objects.filter(actor=slave).update(actor=master)
    Action.objects.filter(target_object_id=slave.id).update(target_object_id=master.id)
    Action.objects.filter(target_object_id=slave.get_profile().id).update(target_object_id=master.get_profile().id)
    Action.objects.filter(action_object_object_id=slave.id).update(action_object_object_id=master.id)
    Action.objects.filter(action_object_object_id=slave.get_profile().id).update(action_object_object_id=master.get_profile().id)
    dares_cr = Dare.objects.filter(creator=slave)
    dares_cr.update(creator=master)

    dare_ch = Dare.objects.filter(challenger=slave)
    dare_ch.update(challenger=master)

    events = Event.objects.filter(creator=slave)
    events.update(creator=master)

    invs = Invitation.objects.filter(sender=slave)
    invs.update(sender=master)

    # notification = Notify.objects.filter(from_user=slave)
    notification.update(from_user=master)
    # Like
    likable_classes = LikableModel.objects.likable_classes
    for klass in likable_classes:
        # Add master into like
        klass.objects.raw_update(
            {
                '_likers': slave.id,
                '_likers': {'$ne': master.id},
            },
            {
                '$addToSet': {'_likers': master.id},
                '$inc': {'_likers_count': 1},
            },
        )
        # Pull slave from like
        klass.objects.raw_update(
            {
                '_likers': slave.id,
            },
            {
                '$pull': {'_likers': slave.id},
                '$inc': {'_likers_count': -1},
            },
        )

    # Updated Model
    privacy_classes = PrivacyRespectingModel.objects.privacy_classes
    update_classes = [TodoItem, Comment, VideoStream]
    update_classes.extend(privacy_classes)
    for klass in update_classes:
        if klass.__name__ != 'UserProfile':
            objs = klass.objects.filter(user=slave)
            objs.update(user=master)
    # Social Profile
    SOCIAL_PROFILE_LIST = [FacebookProfile, WeiboProfile, MixiProfile]
    for SocialProfile in SOCIAL_PROFILE_LIST:
        if SocialProfile.objects.filter(user=slave).exists() and not SocialProfile.objects.filter(user=master).exists():
            objs = SocialProfile.objects.filter(user=slave)
            objs.update(user=master)


class SocialIncorrectOperation(Exception):
    pass


def attatch_social_network(user, social_type, socialAPI):
    if social_type not in SOCIAL_DICTS.keys():
        raise SocialIncorrectOperation('The social_type %s is not in our attatch options.'%social_type)
    socialAPI.attach_local_profile(user=user)
