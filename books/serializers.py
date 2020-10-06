from django.contrib.auth.models import User
from rest_framework.relations import StringRelatedField, SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Books, BookComments


# Serializers define the API representation.
class BookSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'groups']


class BookCommentSerializer(ModelSerializer):

    class Meta:
        model = BookComments
        fields = 'comment', 'book', 'user'

    def to_representation(self, instance):
        rep = super(BookCommentSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username
        rep['book'] = instance.book.title
        return rep
