from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Books(models.Model):
    title = models.CharField('Название', unique=True, max_length=200)
    author_name = models.CharField('Имя автора', null=True, max_length=100)
    description = models.TextField('Описание')
    title_img = models.URLField('Фото обложки')
    link = models.URLField('Ссылка на книгу', blank=True)
    create_date = models.DateField('Дата добавления', auto_now=True)

    def get_absolute_url(self):
        return reverse('book-detail', args=[self.id])

    @property
    def short_description(self):
        return self.description[:10]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BookComments(models.Model):
    comment = models.TextField("Конментарий")
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class SubscriptionsUser(models.Model):
    name = models.CharField('Имя', max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.email
