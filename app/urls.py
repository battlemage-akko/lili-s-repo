from django.urls import re_path, include
from app import views

urlpatterns = [
    re_path('^login_check/',views.login_check,name="login_check")
]