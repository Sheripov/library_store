from django.contrib import admin

from .models import *

admin.site.register(Books, )
admin.site.register(BookComments, )
admin.site.register(SubscriptionsUser, )


