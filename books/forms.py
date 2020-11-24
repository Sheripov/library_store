from django import forms
from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author_name', 'description', 'title_img']


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionsUser
        fields = '__all__'
