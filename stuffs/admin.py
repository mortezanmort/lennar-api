from django.contrib import admin

from .models import Component, Group, Specification

admin.site.register([Component, Group, Specification])
