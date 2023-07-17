from mongoengine import Document
from mongoengine.fields import StringField, ListField, BooleanField, EmailField


class Contacts(Document):
    fullname = StringField()
    email = EmailField()
    phone = ListField()
    sending_preference = StringField()
    is_send = BooleanField(default=False)
