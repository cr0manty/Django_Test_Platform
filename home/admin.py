from django.contrib import admin

from .models import User
from tests.models import UserTestPass


class UserTestPassInline(admin.TabularInline):
    model = UserTestPass


class UsersAdmin(admin.ModelAdmin):
    inlines = [
        UserTestPassInline
    ]


admin.site.register(User, UsersAdmin)
