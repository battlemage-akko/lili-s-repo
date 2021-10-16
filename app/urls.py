from django.urls import re_path, include
from app import views

urlpatterns = [
    re_path('^login_check/',views.login_check,name="login_check"),
    re_path('^register/',views.register,name="register"),
    re_path('^logout/',views.logoutthisuser,name="logout"),
    re_path('^serverDetail/',views.serverDetail,name="serverDetail"),
    re_path('^userDetail/',views.userDetail,name="userDetail"),
    re_path('^getAllUsers/',views.getAllUsers,name="getAllUsers"),
    re_path('^rebootorshutdown/',views.rebootorshutdown,name="rebootorshutdown"),
]