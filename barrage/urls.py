from django.urls import re_path, include
from barrage import views

urlpatterns = [
    re_path('^loadbarrage/',views.loadbarrage,name="loadbarrage"),
    re_path('^save_barrage/',views.save_barrage,name="save_barrage"),
]