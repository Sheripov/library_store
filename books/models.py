from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

import library


class Books(models.Model):
    title = models.CharField('Название', max_length=50)
    author_name = models.CharField('Имя автора', max_length=50)
    description = models.TextField('Описание')

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


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "{0}/{1}".format(self.author.username, self.content[:10])
