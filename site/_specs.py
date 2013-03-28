Flickr
key = "50f2ff50988013ec45a0b52657cff1ac"
secret = "9146dbf617f04a47"


# === Checked ===

0. css, js, html structure
0. Profile Pic

1. Photos
2. Search

0. Friend List (Relation?)
1. Registration, email confirm
2. Facebook Connect
3. Notfication
4. Slug



User:
	=0. Auto Generate UserProfile
	=1. Default Profile Photo
	2. Fullname


	API:
	=1. User info
	2. Search User


Registration:
	=0. Registration
	=1. Verify Username
	=2. Verify email
	=3. Email Confirm Callback
	4. Facebook Connect
	=5. Reset Password
	=6. Resend activation mail
	7. Logout
	=8. Signin


Photo:
	1. 3 Different Photo Size
	2. Get Photo url
	3. Clean Cache when Delete Photo


Site Structure:
	=1. requireJs
	=2. In-site request
	=3. Init Server Data when first load
	4. Base.html
	5. Registration page
	=6. Slug
	7. Remove slug (when there is new "restricted words", we need to change the slug name of origin user or something)
	8. Lightbox


Infra Structure:
	=1. Send Email
	2. Search by Solr
	=3. API Structure
	4. Facebook Connect

Notify:
	1. Structure

	API:
	1. Fetch Notify
	2. Fetch Unread Notify
	3. Set Notify Read