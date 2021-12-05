from django.urls import re_path, include
from barrage import views

urlpatterns = [
    re_path('^loadbarrage/',views.loadbarrage,name="loadbarrage"),
    re_path('^save_barrage/',views.save_barrage,name="save_barrage"),
    re_path('^save_note/',views.save_note,name="save_note"),
    re_path('^save_video/',views.save_video,name="save_video"),
    re_path('^save_compilation/',views.save_compilation,name="save_compilation"),
    re_path('^report/',views.report,name="report"),
    re_path('^getmorenewvideo/',views.getmorenewvideo,name="getmorenewvideo"),
    re_path('^hasbeenplayed/',views.hasbeenplayed,name="hasbeenplayed"),
    re_path('^getMoreCollectVideo/',views.getMoreCollectVideo,name="getMoreCollectVideo"),
    re_path('^getMyVideo/',views.getMyVideo,name="getMyVideo"),
    re_path('^search_video/',views.search_video,name="search_video"),
    re_path('^del_video/',views.del_video,name="delVideo"),
    re_path('^del_Discussion/',views.del_Discussion,name="delDiscussion"),
    re_path('^sendDiscussion/',views.sendDiscussion,name="sendDiscussion"),
    re_path('^sendAnswer/',views.sendAnswer,name="sendAnswer"),
    re_path('^getAllVideoAccusation/',views.getAllVideoAccusation,name="getAllVideoAccusation"),
    re_path('^rejectVideoAccusation/',views.rejectVideoAccusation,name="rejectVideoAccusation"),
    re_path('^updateTags/',views.updateTags,name="updateTags"),
    re_path('^ApplyForV_id/',views.ApplyForV_id,name="ApplyForV_id"),
]
