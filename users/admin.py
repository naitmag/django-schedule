from django.contrib import admin

from users.models import User, Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['number', 'specialization', 'department']
    search_fields = ['number', 'specialization']
    list_filter = ['number', 'department']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_group_number']
    search_fields = ['last_name', 'first_name', 'middle_name']
    list_filter = ['group']
