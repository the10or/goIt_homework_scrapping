from mongoengine import *


class Author(Document):
    fullname = StringField(unique=True)
    born_date = StringField(max_length=100)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author)
    quote = StringField(unique=True)
    meta = {"collection": "quotes"}
