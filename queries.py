from models import Quote, Author


def find_by_tag(tag):
    quotes = Quote.objects(tags__iregex=tag)
    result = [(quote.quote, quote.author.fullname) for quote in quotes]
    return result


def find_by_author(author):
    author = Author.objects(fullname__iregex=author)
    for author in author:
        quotes = Quote.objects(author=author)
        result = [quote.quote for quote in quotes]
        return result, author.fullname
