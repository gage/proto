""" Site photo module forms """

from django import forms
from django.contrib.contenttypes.models import ContentType

from photos.models import Photo

class PhotoForm(forms.ModelForm):
	
	def __init__(self, content_object=None, edit=False, *args, **kwargs):
		super(PhotoForm, self).__init__(*args, **kwargs)
		
		if edit:
			del self.fields['image']
	
	class Meta:
		model = Photo
		fields = ('image', 'title', 'description')

class EventPhotoForm(forms.ModelForm):
	
	class Meta:
		model = Photo
		fields = ('title', 'description')
		widgets = {
			'title': forms.widgets.TextInput(attrs={'class':'txt'}),
			'description': forms.widgets.Textarea(attrs={'class':'txt'})
		}