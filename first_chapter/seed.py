import json
from datetime import datetime
from models import Authors, Quotes
import connect


def add_authors():
    with open('authors.json', 'r') as fh:
        authors = json.load(fh)

    Authors.drop_collection()

    for author in authors:
        Authors(fullname=author['fullname'], born_date=datetime.strptime(author['born_date'], '%B %d, %Y').date(),
                born_location=author['born_location'], description=author['description']).save()


def add_quotes():
    with open('quotes.json', 'r') as fh:
        quotes = json.load(fh)

    authors = Authors.objects()
    Quotes.drop_collection()

    for quote in quotes:
        for author in authors:
            if quote['author'] == author.fullname:
                Quotes(tags=quote['tags'], author=author, quote=quote['quote']).save()


if __name__ == '__main__':
    add_authors()
    add_quotes()
