from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .forms import FileFieldForm, SubscriptionForm
from .models import *
from .tasks import send_spam_email


class BookCreate(LoginRequiredMixin, CreateView):
    model = Books
    fields = ["title", "author_name", "description", "title_img"]


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Books
    fields = ["title", "author_name", "description", "title_img"]


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Books
    success_url = reverse_lazy('book-list')


class BookListView(ListView):
    model = Books
    context_object_name = 'book_list'
    queryset = Books.objects.order_by('-id')


class BookDetailView(DetailView):
    model = Books
    context_object_name = 'book_detail'


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'books/book_upload.html'
    success_url = reverse_lazy('book-list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                import zipfile
                doc = zipfile.ZipFile(f)
                xml_content = doc.read('word/document.xml')
                try:
                    from xml.etree.cElementTree import XML
                except ImportError:
                    from xml.etree.ElementTree import XML
                tree = XML(xml_content)
                paragraphs = []
                WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
                PARA = WORD_NAMESPACE + 'p'
                TEXT = WORD_NAMESPACE + 't'
                for paragraph in tree.iter(PARA):
                    texts = [node.text
                             for node in paragraph.iter(TEXT)
                             if node.text]
                    if texts:
                        paragraphs.append(''.join(texts))
                try:
                    title = paragraphs[0]
                    author_name = paragraphs[1]
                    title_img = paragraphs[2]
                    description = '<br>'.join(paragraphs[3::])

                    Books.objects.create(
                        title=title,
                        author_name=author_name,
                        description=description,
                        title_img=title_img
                    )
                except IntegrityError:
                    print(f, 'SKIPPED')
                    continue
                except IndexError:
                    return render(request, 'books/book_upload.html', {'error': f'{f} - Не соответствует шаблону'})

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SubscriptionCreate(CreateView):
    model = SubscriptionsUser
    form_class = SubscriptionForm
    success_url = '/'
    template_name = 'registration/subscription_form.html'

    def form_valid(self, form):
        form.save()
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)
