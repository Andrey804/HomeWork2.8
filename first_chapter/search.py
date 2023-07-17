import re
import sys
from models import Authors, Quotes
import connect


def checking_was_found(func):
    def inner(value):
        is_found = func(value)

        if not is_found:
            print('Nothing similar found')

    return inner


@checking_was_found
def search_from_name(value, is_found=None):

    authors_id = []
    for res in Authors.objects(fullname__istartswith=value):
        authors_id.append(res.id)

    for res in Quotes.objects(author__in=authors_id):
        is_found = True
        print(f'{res.author.fullname}:\n{res.quote.encode("windows-1251").decode()}')

    return is_found


@checking_was_found
def search_from_tag(value, is_found=None):

    for res in Quotes.objects(tags__startswith=value):
        is_found = True
        print(f'{res.author.fullname}:\n{res.quote.encode("windows-1251").decode()}')

    return is_found


@checking_was_found
def search_from_tags(value_list, is_found=None):

    for res in Quotes.objects(tags__in=value_list):
        is_found = True
        print(f'{res.author.fullname}:\n{res.quote.encode("windows-1251").decode()}')

    return is_found


if __name__ == '__main__':
    while True:
        row_str = input(f'\nEnter the query in the form <command:value> or <command:value1,value2,...>\n>>>').lower()

        if row_str == 'exit':
            sys.exit('Goodbye!')

        elif not re.match('\w+:\w+[\w,]*', row_str):
            print('Wrong input. Try again')
            continue

        command, values = re.split(':', row_str)

        if command == 'name':
            search_from_name(values)

        elif command == 'tag':
            search_from_tag(values)

        elif command == 'tags':
            search_from_tags(re.split(',', values))

        else:
            print('Wrong command. Try again')
            continue
