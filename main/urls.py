from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
                       url(r'^getip/$', views.get_client_ip, name='getip')
                       )
