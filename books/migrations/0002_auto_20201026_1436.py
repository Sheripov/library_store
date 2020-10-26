# Generated by Django 3.1.1 on 2020-10-26 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='author_name',
            field=models.CharField(max_length=100, verbose_name='Имя автора'),
        ),
        migrations.AlterField(
            model_name='books',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]
