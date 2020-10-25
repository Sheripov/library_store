from django.urls import path, re_path

from .views import BookCreate, BookDelete, BookUpdate, BookListView, BookDetailView, FileFieldView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    re_path(r'book_detail/(?P<pk>[0-9]+)/$', BookDetailView.as_view(), name='book-detail'),
    re_path(r'add_book/$', BookCreate.as_view(), name='book-add'),
    re_path(r'book/(?P<pk>[0-9]+)/$', BookUpdate.as_view(), name='book-update'),
    re_path(r'book/(?P<pk>[0-9]+)/delete/$', BookDelete.as_view(), name='book-delete'),
    re_path(r'book_upload/$', FileFieldView.as_view(), name='book-upload'),
]
