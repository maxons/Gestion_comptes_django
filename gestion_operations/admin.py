from django.contrib import admin

from .models import Types, Compte, Operation
# Register your models here.

admin.site.register(Types)
admin.site.register(Compte)
admin.site.register(Operation)
