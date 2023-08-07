import json
from models import Author, Quote
import connect


if __name__ == '__main__':

    # with open('../BS/jsons/authors.json', 'r') as file:
    #     authors_data = json.load(file)
    #
    # with open('../BS/jsons/quotes.json', 'r') as file:
    #     quotes_data = json.load(file)

    with open('../Scrapy/jsons/authors.json', 'r') as file:
        authors_data = json.load(file)

    with open('../Scrapy/jsons/quotes.json', 'r') as file:
        quotes_data = json.load(file)

    for author_data in authors_data:
        author = Author(**author_data)
        author.save()

    for quote_data in quotes_data:
        author_name = quote_data['author']
        author = Author.objects(fullname=author_name).first()

        if author:
            quote_data['author'] = author
            quote = Quote(**quote_data)
            quote.save()


