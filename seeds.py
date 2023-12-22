import json

from mongoengine import NotUniqueError
from pymongo.errors import DuplicateKeyError

from models import Author, Quote
import connect


def seed_authors():
    with open("authors.json", encoding="utf-8") as f:
        authors = json.load(f)

    for author in authors:
        try:
            Author(
                fullname=author["fullname"],
                born_date=author["born_date"],
                born_location=author["born_location"],
                description=author["description"],
            ).save()
        except NotUniqueError:
            print(f'Author {author["fullname"]} already exists, skipping...')


def seed_quotes():
    with open("quotes.json", encoding="utf-8") as f:
        quotes = json.load(f)

        for quote in quotes:
            try:
                Quote(
                    tags=quote["tags"],
                    author=Author.objects(fullname=quote["author"]).first(),
                    quote=quote["quote"].encode("utf-8"),
                ).save()
            except (NotUniqueError, DuplicateKeyError):
                print(f'Quote {quote["quote"]} already exists, skipping...')


if __name__ == "__main__":
    seed_authors()
    seed_quotes()
