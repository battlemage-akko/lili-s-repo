"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from app import views
from app import urls as app_api
from barrage import urls as video_api
from django.views.generic import TemplateView
from order_channels import views as channelsviews
from barrage import views as barrageView
urlpatterns = [
    #path('admin/', admin.site.urls),
    # url(r'^static/(?P<path>.*)$', static.serve,
    #   {'document_root': settings.STATIC_ROOT}, name='static'),
    path('test/', views.test, name="test"),
    path('null/', channelsviews.channelsviews, name="null"),
    path('testvue/', TemplateView.as_view(template_name="index.html")),
    path('login/', views.index_login, name="login"),
    path('',views.index,name="index"),
    path('video/<int:vid>',barrageView.video,name="video"),
    re_path('^upload_page/', views.upload_page, name="upload_page"),
    re_path('^app_api/', include(app_api)),
    re_path('^video_api/', include(video_api))
]
