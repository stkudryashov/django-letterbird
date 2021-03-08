from django.contrib import admin
from .models import Letter


class LetterAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'views', 'saves', 'datetime']


admin.site.register(Letter, LetterAdmin)
