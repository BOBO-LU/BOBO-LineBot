from django.contrib import admin
from application.models import users

class usersAdmin(admin.ModelAdmin):
    list_disply = ('uid', 'datatest')

admin.site.register(users, usersAdmin)
