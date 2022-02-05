from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Follow

User = get_user_model()

UserAdmin.list_filter = ('username', 'email')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
