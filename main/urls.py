from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.login, name='login'),
                        url(r'^logout/$', views.logout, name='logout')
                       )
