from django.urls import re_path, include,path
from app import views

urlpatterns = [
    path('getNameAndPic',views.getNameAndPic,name="getNameAndPic"),
    path('java_checkAuther',views.java_checkAuther,name="java_checkAuther"),
    re_path('^login_check/',views.login_check,name="login_check"),
    re_path('^register/',views.register,name="register"),
    re_path('^logout/',views.logoutthisuser,name="logout"),
    re_path('^serverDetail/',views.serverDetail,name="serverDetail"),
    re_path('^userDetail/',views.userDetail,name="userDetail"),
    re_path('^getAllUsers/',views.getAllUsers,name="getAllUsers"),
    re_path('^rebootorshutdown/',views.rebootorshutdown,name="rebootorshutdown"),
    re_path('^Del_user/',views.Del_user,name="Del_user"),
    re_path('^refreshmsg/',views.refreshmsg,name="refreshmsg"),
    re_path('^clearmsg/',views.clearmsg,name="clearmsg"),
    re_path('^follow/',views.follow,name="follow"),
    re_path('^love/',views.love,name="love"),
    re_path('^collect/',views.collect,name="collect"),
    re_path('^save_profile/',views.save_profile,name="save_profile"),
    re_path('^save_background/',views.save_background,name="save_background"),
    re_path('^save_avatar/',views.save_avatar,name="save_avatar"),
    re_path('^getFans/',views.getFans,name="getFans"),
    re_path('^getHotestVideos/',views.getHotestVideos,name="getHotestVideos"),
]