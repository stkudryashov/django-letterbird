from django.contrib import admin
from .models import Letter


class LetterAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'author', 'views', 'saves', 'datetime']
    list_display_links = ['id', '__str__']


admin.site.register(Letter, LetterAdmin)
