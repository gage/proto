from django.conf import settings

class APIException(Exception):
    def __init__(self, code, debug=None):
        self.code = code
        self.debug = debug

ERROR_GENERAL_NO_ERROR                  = 00000 #: No error
ERROR_GENERAL_UNKNOWN_ERROR             = 10000 #: Last ditch error, unkown cause
ERROR_GENERAL_BAD_SIGNATURE             = 10001 #: Request parameters don't match method signature
ERROR_GENERAL_NOT_FOUND                 = 10002 #: Resource does not exist
ERROR_GENERAL_USER_NOT_FOUND            = 10003 #: User does not exist
ERROR_GENERAL_BAD_TYPE                  = 10004 #: Content type does not exist
ERROR_GENERAL_TARGET_NOT_FOUND          = 10005 #: Target object not found
ERROR_GENERAL_BAD_ID_FORMAT             = 10006 #: Bad ID format
ERROR_GENERAL_INVALID_OPERATION         = 10007 #: Not effective operation (already done or not allowed)
ERROR_GENERAL_BAD_PARA_FORMAT           = 10008 #: Some requested parameters are not valid
ERROR_AUTH_NOT_AUTHENTICATED            = 10100 #: Requested authenticated resource anonymously
ERROR_AUTH_BAD_CREDENTIALS              = 10101 #: Bad username/password combo
ERROR_AUTH_NOT_AUTHORIZED               = 10102 #: Not authorized resource access
ERROR_AUTH_PASSWORD_CONFIRM_NOT_MATCH   = 10103 #: Passwords do not match.
ERROR_AUTH_NO_PASSWORD                  = 10104 #: No password
ERROR_AUTH_PASSWORD_INVALID             = 10105 #: The password should be between 6 to 20 characters
ERROR_AUTH_USER_ALREADY_LOGIN           = 10106 #: User already log in
ERROR_AUTH_USER_ALREADY_ACTIVATED       = 10107 #: User have already been activated
ERROR_AUTH_USER_CANNT_CHANGE_USERNAME   = 10108 #: User can't change username anymore
ERROR_AUTH_USER_EMAIL_NOT_EXIST         = 10109 #: Email does not exist
ERROR_AUTH_USER_NO_GROUP                = 10110 #: User have to create group before logging in
ERROR_AUTH_PASSWORD_CONFIRM_INVALID     = 10111 #: The confirmation password should be between 6 to 20 characters
ERROR_AUTH_USERNAME_NOT_EXIST           = 10112 #: The username you entered does not exist
ERROR_USER_PASSWORD_NOT_MATCH           = 10200 #: Incorrect password
ERROR_USER_FREIND_REQUEST_NOT_FOUND     = 10201 #: Friend request is not found
ERROR_USER_INVALID_FEEDBACK             = 10202 #: Feedback cannot be empty
ERROR_REGISTRATION_INVALID_USERNAME     = 10300 #: Invalid username format
ERROR_REGISTRATION_USERNAME_UNAVAILABLE = 10301 #: Username already in use or restricted
ERROR_REGISTRATION_EMAIL_USED           = 10302 #: Email already in use
ERROR_REGISTRATION_INVALID_EMAIL        = 10303 #: Invalid email address format
ERROR_REGISTRATION_NOT_ACTIVATE         = 10304 #: The user is not activated
ERROR_REGISTRATION_INVALID_FULLNAME     = 10305 #: Invalid fullname format
ERROR_REGISTRATION_NOT_REGIST_YET       = 10306 #: The user has not registed yet.
ERROR_REGISTRATION_PHONE_CODE_NOT_MATCH = 10307 #: The phone registration code does not match.

ERROR_FACEBOOK_INVALID_TOKEN            = 10400 #: Access token invalid or expired
ERROR_FACEBOOK_BAD_CREDENTIALS          = 10401 #: Bad facebook ID/access token combination
ERROR_FACEBOOK_BAD_REQUEST              = 10402 #: Expired facebook ID/access token combination
ERROR_FACEBOOK_NO_PROFILE               = 10403 #: You should do facebook connect first.
ERROR_PHOTOS_TOO_LARGE                  = 10500 #: Photo data exceeds filesize limit.  Limit can be configured in settings.PHOTOS_MAX_SIZE
ERROR_PHOTOS_BAD_FORMAT                 = 10501 #: Photo data not in accepted format.  Accepted formats can be configured in settings.PHOTOS_FORMATS
ERROR_PHOTOS_NO_IMAGE                   = 10502 #: No image could be decoded.
ERROR_PHOTOS_BROKEN_LINK                = 10503 #: The link given by user is not valid
ERROR_PHOTOS_BASE64_DECODE_FAILED       = 10504 #: Problem occurred while saving photo
ERROR_VIDEO_NO_VIDEO                    = 10600 #: No video could be read.
ERROR_WEIBO_INVALID_TOKEN               = 10700 #: Access token invalid or expired
ERROR_FOLDER_REPLICA_NAME               = 10800 #: Replica name with other folder
ERROR_FILE_REPLICA_NAME                 = 10801 #: Replica name with other file
ERROR_FILE_INVALID_FORMAT               = 10802 #: Invalid file format
ERROR_FOLDER_CANNOT_BE_SHARED           = 10803 #: There are other shared folders in this folder
ERROR_FOLDER_NOT_FOUND                  = 10804 #: The requested folder is not found
ERROR_FOLDER_CANNOT_BE_MOVED            = 10805 #: The moved folder contains shared folder, and it cannot be moved into other shared folder.
ERROR_FOLDER_EXCEED_QUOTA               = 10806 #: The space usage exceeds quota.
ERROR_FILE_NOT_FOUND                    = 10807 #: The requested file is not found
ERROR_FOLDER_INVALID_NAME               = 10808 #: The name is invalid for a folder.
ERROR_FILE_INVALID_NAME                 = 10809 #: The name is invalid for a file.
ERROR_FOLDER_DESTINATION_NOT_ALLOWED    = 10810 #: The destinetion of this folder is not legal
ERROR_DROPBOX_PROFILE_NOT_FOUND         = 10900 #: The dropbox profile is not found.
ERROR_DROPBOX_NOT_AUTH                  = 10901 #: The dropbox client is not authenticated.
ERROR_DROPBOX_FILE_NOT_FOUND            = 10902 #: The dropbox file is not found.
ERROR_DROPBOX_NO_UPDATE                 = 10903 #: The dropbox file is not found.
ERROR_GROUP_NOT_BEEN_INVITED            = 11000 #: The user is not invited by this group
ERROR_GROUP_NOT_MEMBER                  = 11001 #: The user is not a member of this group
ERROR_GROUP_NOT_TEMPORARY               = 11002 #: The group is not a temporary group 
ERROR_SHARE_NOT_FOUND                   = 11100 #: No share object
ERROR_SHARE_REPEAT_TWITTER_MSG          = 11101 #: Repeat twitter message
ERROR_INVALID_SLUG                      = 11200 #: Invalid slug 
ERROR_INSTAGRAM_NO_PROFILE              = 11300 #: No instagram profile
ERROR_MESSAGE_NOT_FOUND                 = 11400 #: Invalid slug 
ERROR_CARD_NOT_IN_BOOK                  = 11500 #: Card not in book
ERROR_EVENT_USER_NOT_INVITED            = 11600 #: User is not invited to the event
ERROR_BLOG_EMPTY_TITLE                  = 10700 #: Blog title cannot be empty
ERROR_BLOG_EMPTY_CONTENT                = 10701 #: Blog content cannot be empty
ERROR_IOS_TOKEN_INVALID                 = 11701 #: Blog content cannot be empty
ERROR_CHATROOM_NOT_EDITABLE             = 11800 #: Chatroom is not editable
ERROR_CHATROOM_NAME_TOO_LONG            = 11801 #: Chatroom name should be shorter than 30 chars
ERROR_LINK_INVALID_URL                  = 11901 #: The Url is invalid.
ERROR_YOUTUBE_QUERY_PARA_NOT_MATCH      = 12100 #: The parameters of youtube api is not correct

API_ERRORS = {
    ERROR_GENERAL_NO_ERROR: "No Error.",
    ERROR_GENERAL_UNKNOWN_ERROR: "Unknown error.  Please contact API team.",
    ERROR_GENERAL_BAD_SIGNATURE: "Method signature does not match.",
    ERROR_GENERAL_NOT_FOUND: "Page not found.",
    ERROR_GENERAL_USER_NOT_FOUND: "User could not be found.",
    ERROR_GENERAL_BAD_TYPE: "Content type is invalid or does not exist.",
    ERROR_GENERAL_TARGET_NOT_FOUND: "Target object does not exist.",
    ERROR_GENERAL_BAD_ID_FORMAT : "Bad ID format.",
    ERROR_GENERAL_INVALID_OPERATION : "Not effective operation (already done or not allowed).",
    ERROR_GENERAL_BAD_PARA_FORMAT : "Some requested parameters are not valid.",
    ERROR_AUTH_NOT_AUTHENTICATED: "Authentication required.",
    ERROR_AUTH_BAD_CREDENTIALS: "Invalid username/password combination.",
    ERROR_AUTH_NOT_AUTHORIZED: "The request user is not authorized to access this resource.",
    ERROR_AUTH_PASSWORD_CONFIRM_NOT_MATCH: "Passwords do not match.",
    ERROR_AUTH_NO_PASSWORD: "Password should not be empty.",
    ERROR_AUTH_PASSWORD_INVALID: "The password should be between 6 to 20 characters.",
    ERROR_AUTH_USER_ALREADY_LOGIN: "User have already logged in.",
    ERROR_AUTH_USER_ALREADY_ACTIVATED: "User have already been activated.",
    ERROR_AUTH_USER_CANNT_CHANGE_USERNAME: "User can't change username anymore.",
    ERROR_AUTH_USER_EMAIL_NOT_EXIST: "Email does not exist.",
    ERROR_AUTH_USER_NO_GROUP: "You have to create group before logging in",
    ERROR_AUTH_PASSWORD_CONFIRM_INVALID: "The confirmation password should be between 6 to 20 characters.",
    ERROR_AUTH_USERNAME_NOT_EXIST: "The username you entered does not exist",
    ERROR_USER_PASSWORD_NOT_MATCH: "Incorrect password.",
    ERROR_USER_FREIND_REQUEST_NOT_FOUND : "Friend request is not found",
    ERROR_USER_INVALID_FEEDBACK : "Feedback cannot be empty",
    ERROR_REGISTRATION_INVALID_USERNAME: "Invalid username.  Usernames must contain letters or numbers, between 5 and 15 characters. Cannot contain '-', ' ' and cannot start with '_'.",
    ERROR_REGISTRATION_INVALID_FULLNAME: "Full name must contain letters or numbers, between 1 and 60 characters.",
    ERROR_REGISTRATION_USERNAME_UNAVAILABLE: "This username is unavailable.",
    ERROR_REGISTRATION_EMAIL_USED: "This email address is already in use.",
    ERROR_REGISTRATION_INVALID_EMAIL: "Invalid email address format.",
    ERROR_REGISTRATION_NOT_ACTIVATE : "The user is not activated.",
    ERROR_REGISTRATION_NOT_REGIST_YET : "The user has not registed yet.",
    ERROR_REGISTRATION_PHONE_CODE_NOT_MATCH : "The phone registration code does not match.",
    ERROR_FACEBOOK_INVALID_TOKEN: "Facebook access token invalid or expired.",
    ERROR_FACEBOOK_BAD_CREDENTIALS: "Bad facebook ID/access token combination.",
    ERROR_FACEBOOK_BAD_REQUEST: "Expired facebook ID/access token combination. Please ask for token again.",
    ERROR_FACEBOOK_NO_PROFILE: "You should do facebook connect first.",
    ERROR_PHOTOS_TOO_LARGE: "Photo exceeds %s byte filesize limit." % settings.PHOTOS_MAX_SIZE,
    ERROR_PHOTOS_BAD_FORMAT: "Bad photo format.  Accepted formats are (%s)." % ",".join(settings.PHOTOS_FORMATS),
    ERROR_PHOTOS_NO_IMAGE: "No image could be decoded.",
    ERROR_PHOTOS_BROKEN_LINK: "The link given by user is not valid.",
    ERROR_PHOTOS_BASE64_DECODE_FAILED: "Problem occurred while saving photo",
    ERROR_VIDEO_NO_VIDEO: "No video could be read.",
    ERROR_WEIBO_INVALID_TOKEN: "Access token invalid or expired",
    ERROR_FOLDER_REPLICA_NAME: "Replica name with other folder",
    ERROR_FILE_REPLICA_NAME: "Replica name with other file",
    ERROR_FILE_INVALID_FORMAT: "Invalid file format",
    ERROR_FOLDER_CANNOT_BE_SHARED: "There are other shared folders in this folder",
    ERROR_FOLDER_NOT_FOUND: "The requested folder is not found",
    ERROR_FOLDER_CANNOT_BE_MOVED: "The moved folder contains shared folder, and it cannot be moved into other shared folder.",
    ERROR_FOLDER_EXCEED_QUOTA: "The space usage exceeds quota",
    ERROR_FILE_NOT_FOUND: "The requested file is not found",
    ERROR_FOLDER_INVALID_NAME: "The name is invalid for a folder.",
    ERROR_FILE_INVALID_NAME: "The name is invalid for a file.",
    ERROR_FOLDER_DESTINATION_NOT_ALLOWED: "The destinetion of this folder is not legal",
    ERROR_DROPBOX_PROFILE_NOT_FOUND: "The dropbox profile is not found.",
    ERROR_DROPBOX_NOT_AUTH: "The dropbox client is not authenticated.",
    ERROR_DROPBOX_FILE_NOT_FOUND: "The dropbox file is not found.",
    ERROR_GROUP_NOT_BEEN_INVITED: "The user is not invited by this group",
    ERROR_GROUP_NOT_MEMBER: "The user is not a member of this group",
    ERROR_GROUP_NOT_TEMPORARY: "The group is not a temporary group",
    ERROR_SHARE_NOT_FOUND: "No share object",
    ERROR_SHARE_REPEAT_TWITTER_MSG: "Repeat twitter message",
    ERROR_INVALID_SLUG: "Invalid slug",
    ERROR_INSTAGRAM_NO_PROFILE: "No instagram profile",
    ERROR_MESSAGE_NOT_FOUND: "No Message object",
    ERROR_CARD_NOT_IN_BOOK: "Card not in book",
    ERROR_EVENT_USER_NOT_INVITED: "User is not invited to the event",
    ERROR_BLOG_EMPTY_TITLE: "Blog title cannot be empty",
    ERROR_BLOG_EMPTY_CONTENT: "Blog content cannot be empty",
    ERROR_IOS_TOKEN_INVALID: "The IOS token is invalid",
    ERROR_CHATROOM_NOT_EDITABLE: "Chatroom is not editable",
    ERROR_CHATROOM_NAME_TOO_LONG: "Chatroom name should be shorter than 30 chars",
    ERROR_LINK_INVALID_URL: "The URL is invalid",
    ERROR_YOUTUBE_QUERY_PARA_NOT_MATCH: "The parameters of youtube api is not correct",
}
