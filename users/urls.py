from django.urls import path, re_path

from users import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    re_path(r'profile_update/$', views.UserUpdate.as_view(), name='profile_update'),
    re_path(r'profile_detail/$', views.UserDetail.as_view(), name='profile-detail'),
]
