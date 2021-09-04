from django.contrib import admin
from django.apps import apps

from .models import ExtendedUser, Security, Portfolio

admin.site.register(ExtendedUser)
admin.site.register(Security)
admin.site.register(Portfolio)

