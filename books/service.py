import bs4
import requests
from django.core.mail import send_mail
from books.models import Books


class Send:
    def __init__(self, user_email):
        send_mail(
            'Вы подписались на спам',
            'Хахахаха',
            'farbest1995@gmail.com',
            [user_email],
            fail_silently=False,
        )


class ParsingAndAddBooks:
    def __init__(self, url: str = 'https://oz.by/books/bestsellers?sort=novelty_desc'):
        r = requests.get(url)
        self.soup = bs4.BeautifulSoup(r.text, 'html.parser')
        self.add_to_db(self.data_to_model(*self.parsing(self.soup)))

    @staticmethod
    def is_the_only_string_within_a_tag(str_):
        """Return True if this string is the only child of its parent tag."""
        return str_ == str_.parent.string

    def parsing(self, soup):
        books_url = []
        books_img = []
        books_title = []
        books_author = []
        books_description = []
        for book_list in soup.find_all('div', {'class': 'mn-layout__col-2__inner'}):
            for book_url in book_list.find_all(
                    'a',
                    {'class': 'needsclick item-type-card__link item-type-card__link--main'}
            ):
                url_book = f"https://oz.by{book_url.get('href')}"
                books_url.append(url_book)
                r_book = requests.get(url_book)
                soup_book = bs4.BeautifulSoup(r_book.text, 'html.parser')
                tmp_img, tmp_title = self.get_img_and_title(soup_book)
                books_img.append(tmp_img)
                books_title.append(tmp_title)
                books_author += self.get_author(soup_book)
                books_description += self.get_description(soup_book)
            return books_url, books_img, books_title, books_author, books_description

    @staticmethod
    def get_img_and_title(soup_book):
        for img in soup_book.find_all('div', {'class': 'b-product-photo__picture-self'}):
            books_img = img.img.get('src')
            books_title = img.img.get('title')
            return books_img, books_title

    def get_author(self, soup_book) -> list:
        books_author = []
        for author in soup_book.find_all('div', {'class': 'b-product-title__author'}):
            if author.a:
                books_author.append(author.find_all(string=self.is_the_only_string_within_a_tag))
            else:
                books_author.append(None)
        return books_author

    def get_description(self, soup_book) -> list:
        books_description = []
        for description in soup_book.find_all('div', {'class': 'b-description__sub'}):
            if description.p:
                books_description.append(description.find_all(string=self.is_the_only_string_within_a_tag))
                break
            else:
                books_description.append(None)
        return books_description

    @staticmethod
    def join_only_no_null(list_: list) -> str:
        try:
            return '<br>'.join(list_)
        except TypeError:
            return ''

    def data_to_model(self,
                      books_url: list,
                      books_img: list,
                      books_title: list,
                      books_author: list,
                      books_description: list,
                      ) -> list:
        books_list = []
        for i in range(len(books_url)):
            book_info = {
                'url': books_url[i],
                'img': books_img[i],
                'title': books_title[i],
                'author': self.join_only_no_null(books_author[i]),
                'description': self.join_only_no_null(books_description[i])
            }
            books_list.append(book_info)
        return books_list

    @staticmethod
    def add_to_db(books_list: list):
        books = []
        for book in books_list:
            books.append(Books(
                title=book['title'],
                title_img=book['img'],
                description=book['description'],
                author_name=book['author'],
                link=book['url'],
            ))
        Books.objects.bulk_create(books, ignore_conflicts=True)
