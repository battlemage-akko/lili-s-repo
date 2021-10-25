from django.urls import re_path, include
from barrage import views

urlpatterns = [
    re_path('^loadbarrage/',views.loadbarrage,name="loadbarrage"),
    re_path('^save_barrage/',views.save_barrage,name="save_barrage"),
    re_path('^save_video/',views.save_video,name="save_video"),
    re_path('^getmorehotvideo/',views.getmorehotvideo,name="getmorehotvideo"),
    re_path('^hasbeenplayed/',views.hasbeenplayed,name="hasbeenplayed"),
]