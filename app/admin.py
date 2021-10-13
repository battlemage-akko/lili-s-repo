from django.contrib import admin
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import AppUser

admin.site.register(AppUser,UserAdmin)