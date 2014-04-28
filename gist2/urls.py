from django.conf.urls import patterns, url
from gist2 import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^gists/(?P<gist_id>\d+)/$', views.details_gist, name='detail_gist'),
	url(r'^users/(?P<user_id>\d+)/$', views.details_user, name='detail_user'),
	url(r'^users/(?P<user_id>\d+)/gists/$', views.user_gists, name='user_gists'),
)

