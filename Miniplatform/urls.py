"""Miniplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app import views
from app import api

 



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.Index,name='index'),
    url(r'^addhost/$',views.Add_hosts,name='addhost'),
    url(r'^gethosts/$',api.assets_list,name='assetslist'),
    url(r'^getdatas/$',api.data_list,name='datalist'),
    url(r'^mysqlline/$',api.dbstat_list,name='dblist'),
    url(r'^info/ip/(\d+)/$',views.Host_details,name='hostdetail'),
    url(r'^info/ip/(?P<hid>\d+)/(?P<interval>\d+)/$',views.get_history_data,name='gethistorydata'),
    url(r'^info/dbstat/(\d+)/$',views.Mysql_details,name='getdbdetail'),
    url(r'^info/dbstat/(?P<hid>\d+)/(?P<interval>\d+)/$',views.get_mysql_data,name='getmysqldata'),
    url(r'^test/(\d+)/$',views.get_table_test,name='gettabletest'),
]
