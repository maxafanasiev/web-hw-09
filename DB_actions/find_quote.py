import connect
from models import Author, Quote
from redis_cache import cache


@cache
def search_quotes(query):
    if query.startswith('name: '):
        author_name = query[6:]
        author = Author.objects(fullname__icontains=author_name).first()
        if author:
            quotes_ = Quote.objects(author=author)
            return quotes_
    elif query.startswith('tag:'):
        tag = query[4:]
        quotes_ = Quote.objects(tags__icontains=tag)
        return quotes_
    elif query.startswith('tags:'):
        tags = query[5:].split(',')
        quotes_ = Quote.objects(tags__in=tags)
        return quotes_
    else:
        return []


if __name__ == '__main__':
    while True:
        user_input = input('Enter command: ')
        if user_input == 'exit':
            break

        quotes = search_quotes(user_input)
        for quote in quotes:
            author_fullname = quote.author.fullname
            quote_text = quote.quote
            author_utf8 = author_fullname.encode('utf-8').decode('utf-8')
            quote_text_utf8 = quote_text.encode('utf-8').decode('utf-8')

            print(f'Author: {quote.author.fullname}')
            print(f'Tags: {", ".join(quote.tags)}.')
            print(f'Quote: {quote.quote}')
            print('-'*50)
