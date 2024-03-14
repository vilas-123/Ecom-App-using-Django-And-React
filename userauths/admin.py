from django.contrib import admin
from  userauths.models import (User, Profile)


class UserAdmin(admin.ModelAdmin):
    list_display = ['fullname','email','phone']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname','gender','country']

admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)

