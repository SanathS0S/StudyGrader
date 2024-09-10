from django.contrib import admin

# Register your models here.
from .models import Teachers,Students,Marks

admin.site.register(Teachers)
admin.site.register(Students)
admin.site.register(Marks)