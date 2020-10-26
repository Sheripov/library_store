from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.views import generic
from rest_framework.reverse import reverse_lazy


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserUpdate(LoginRequiredMixin, generic.UpdateView):
    def dispatch(self, request, *args, **kwargs):
        self.kwargs = {"pk": self.request.user.pk}
        return super(UserUpdate, self).dispatch(request, *args, **kwargs)

    model = User
    template_name = 'registration/user_update.html'
    fields = "username", "first_name", "last_name", "email"
    success_url = reverse_lazy('profile-detail')


class UserDetail(LoginRequiredMixin, generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        self.kwargs = {"pk": self.request.user.pk}
        return super(UserDetail, self).dispatch(request, *args, **kwargs)

    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user_detail'
