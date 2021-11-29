from django.urls import re_path, include,path
from setting import views

urlpatterns = [
    path('',views.setting_profile),
    re_path('^setting_profile/', views.setting_profile,name="setting_profile"),
    re_path('^setting_avatar/', views.setting_avatar,name="setting_avatar"),
]