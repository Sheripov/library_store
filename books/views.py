from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.dateformat import DateFormat, TimeFormat
from django.utils.formats import get_format
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Books


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'polls.can_add'
    model = Books
    fields = ["title", "author_name", "description"]


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'polls.can_edit'
    model = Books
    fields = ["title", "author_name", "description"]


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'polls.can_delete'
    model = Books
    success_url = reverse_lazy('book-list')


class BookListView(ListView):
    model = Books
    context_object_name = 'book_list'
    queryset = Books.objects.order_by('-id')


class BookDetailView(DetailView):
    model = Books
    context_object_name = 'book_detail'
    context = super(BookDetailView, self).get_context_data()
    context["comment_form"] = CommentForm()


class CommentSavingView(LoginRequiredMixin, View):

    template_name = "books/books_detail"

    def post(self, request, *args, **kwargs):
        book_id = self.request.POST.get("book_id")
        comment = self.request.POST.get("comment")
        book = Books.objects.get(pk=book_id)
        new_comment = book.comments.create(author=request.user, content=comment)
        dt = datetime.now()
        df = DateFormat(dt)
        tf = TimeFormat(dt)
        new_comment_timestamp = (
            df.format(get_format("DATE_FORMAT"))
            + ", "
            + tf.format(get_format("TIME_FORMAT"))
        )
        data = [
            {
                "author": new_comment.author.get_full_name(),
                "comment": new_comment.content,
                "comment_id": new_comment.pk,
                "timestamp": new_comment_timestamp,
            }
        ]
        return JsonResponse(data, safe=False)