from django.urls import re_path, include,path
from setting import views

urlpatterns = [
    path('',views.setting_info),
    re_path('^setting_profile/', views.setting_profile,name="setting_profile"),
    re_path('^setting_avatar/', views.setting_avatar,name="setting_avatar"),
    re_path('^setting_info/', views.setting_info,name="setting_info"),
    re_path('^setting_password/', views.setting_password,name="setting_password"),
    re_path('^password_check/', views.password_check,name="password_check"),
    re_path('^change_password/', views.change_password,name="change_password"),
    re_path('^getMySetting/', views.getMySetting,name="getMySetting"),
    re_path('^changeMySetting/', views.changeMySetting,name="changeMySetting"),
]