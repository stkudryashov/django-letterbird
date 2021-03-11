from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import gettext_lazy as _

from letters.models import Letter
from .models import User


class LetterInline(admin.StackedInline):
    model = Letter
    extra = 0


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        ('Статистика', {
            'fields': ('recently', 'bookmarks', 'current_letter'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
    )

    # inlines = [LetterInline]
    filter_horizontal = ('recently', 'bookmarks', 'user_permissions')
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(User, MyUserAdmin)
