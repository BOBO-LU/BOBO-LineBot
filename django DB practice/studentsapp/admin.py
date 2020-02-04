from django.contrib import admin
from studentsapp.models import student

class studentAdmin(admin.ModelAdmin) :
    list_display = ( 'id', 'cName', 'cSex', 'cEmail', 'cBirthday', 'cPhone', 'cAddr' ) #顯示多個欄位
    list_filter = ( 'cName', 'cSex', ) #建立過濾欄位
    search_fields = ( 'cName', ) #依照欄位搜尋
    ordering = ( 'id', ) #排序

admin.site.register(student,studentAdmin)   