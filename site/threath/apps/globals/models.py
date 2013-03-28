import datetime
import uuid
import hashlib

from django import forms
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from djangotoolbox.fields import ListField


class StringListField(forms.CharField):
    def prepare_value(self, value):
        if value:
            return ', '.join([str(v) for v in value])

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]


class ListFieldEditableInAdmin(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)

