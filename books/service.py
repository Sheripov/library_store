import bs4 as bs4
import requests
from django.core.mail import send_mail
from django.db import IntegrityError

from books.models import Books


def send(user_email):
    send_mail(
        'Вы подписались на спам',
        'Хахахаха',
        'farbest1995@gmail.com',
        [user_email],
        fail_silently=False,
    )


def parsing_and_add_books():
    url = 'https://oz.by/books/bestsellers?sort=novelty_desc'
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    def is_the_only_string_within_a_tag(s):
        """Return True if this string is the only child of its parent tag."""
        return s == s.parent.string

    books_list = []
    books_url = []
    books_img = []
    books_title = []
    books_author = []
    books_description = []
    for book_list in soup.find_all('div', {'class': 'mn-layout__col-2__inner'}):
        for book_url in book_list.find_all('a',
                                           {'class': 'needsclick item-type-card__link item-type-card__link--main'}):
            urlbook = f"https://oz.by{book_url.get('href')}"
            books_url.append(urlbook)
            r_book = requests.get(urlbook)
            soup_book = bs4.BeautifulSoup(r_book.text, 'html.parser')
            for img in soup_book.find_all('div', {'class': 'b-product-photo__picture-self'}):
                books_img.append(img.img.get('src'))
                books_title.append(img.img.get('title'))
                break
            for author in soup_book.find_all('div', {'class': 'b-product-title__author'}):
                if author.a:
                    books_author.append(author.find_all(string=is_the_only_string_within_a_tag))
                else:
                    books_author.append(None)
            for description in soup_book.find_all('div', {'class': 'b-description__sub'}):
                if description.p:
                    books_description.append(description.find_all(string=is_the_only_string_within_a_tag))
                    break
                else:
                    books_description.append(None)

    def join_only_no_null(list):
        try:
            return '<br>'.join(list)
        except TypeError:
            return ''

    for i in range(len(books_url)):
        book_info = {
            'url': books_url[i],
            'img': books_img[i],
            'title': books_title[i],
            'author': join_only_no_null(books_author[i]),
            'description': join_only_no_null(books_description[i])
        }
        books_list.append(book_info)

    for book in books_list:
        try:
            Books.objects.create(
                title=book['title'],
                title_img=book['img'],
                description=book['description'],
                author_name=book['author'],
                link=book['url'],
            )
        except IntegrityError:
            print(book['url'], 'SKIPPED')
            continue
