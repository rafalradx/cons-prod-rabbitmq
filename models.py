from enum import Enum

from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, EnumField, EmailField


class PreferedMessage(Enum):
    SMS = "sms"
    EMAIL = "email"


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField()
    message_sent = BooleanField(default=False)
    contact_via = EnumField(PreferedMessage, default=PreferedMessage.EMAIL)
