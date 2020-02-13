from django.contrib import admin
from application.models import users

class usersAdmin(admin.ModelAdmin):
    list_disply = ('uid', 'datatest', 'chat_mode')

admin.site.register(users, usersAdmin)
