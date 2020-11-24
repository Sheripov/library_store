from django.core.mail import send_mail
from library.celery import app
from .models import SubscriptionsUser, Books
from .service import send, parsing_and_add_books



@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task
def send_beat_email():
    for contact in SubscriptionsUser.objects.all():
        send_mail(
            'Прошу! Спам!',
            'Ваш СПАМ!)',
            'farbest1995@gmail.com',
            [contact.email],
            fail_silently=False,
        )


@app.task
def add_books_from_site():
    parsing_and_add_books()
