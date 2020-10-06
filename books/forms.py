from django.forms import ModelForm, forms

from .models import Books


class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author_name', 'description', 'title_img']


class CommentForm(forms.Form):

    comment = forms.CharField(widget=forms.Textarea)
