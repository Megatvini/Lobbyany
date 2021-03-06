from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^loginForm/$', views.logH, name='logH'),
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^getplaylist/$', views.getplaylist, name='getplaylist'),
                       url(r'^isadmin/$', views.isadmin, name='isadmin'),
                       url(r'^vote/$', views.vote, name='vote'),
                       url(r'^addsong/$', views.addsong, name='addsong'),
                       url(r'^playnext/$', views.playnext, name='playnext'),
                       )
