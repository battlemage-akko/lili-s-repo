from django.urls import re_path, include
from barrage import views

urlpatterns = [
    re_path('^loadbarrage/',views.loadbarrage,name="loadbarrage"),
    re_path('^save_barrage/',views.save_barrage,name="save_barrage"),
    re_path('^save_video/',views.save_video,name="save_video"),
    re_path('^del_video/',views.del_video,name="delVideo"),
    re_path('^getmorenewvideo/',views.getmorenewvideo,name="getmorenewvideo"),
    re_path('^hasbeenplayed/',views.hasbeenplayed,name="hasbeenplayed"),
    re_path('^getMoreCollectVideo/',views.getMoreCollectVideo,name="getMoreCollectVideo"),
    re_path('^getmyvideo/',views.getmyvideo,name="getmyvideo"),
]