from django.conf.urls import patterns, url
from gist2 import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<page>\d*)$', views.index, name='index'),
	url(r'^gists/(?P<gist_id>\d+)/$', views.detail_gist, name='detail_gist'),
	url(r'^users/(?P<user_id>\d+)/$', views.detail_user, name='detail_user'),
	url(r'^users/(?P<user_id>\d+)/(?P<page>\d+)/$', views.detail_user, name='detail_user'),
	url(r'^users/(?P<user_id>\d+)/remove$', views.remove_user, name='remove_user'),
	url(r'^users/(?P<user_id>\d+)/update$', views.update_user, name='update_user'),
	url(r'^gists/(?P<gist_id>\d+)/edit$', views.edit_gist, name='edit_gist'),
	url(r'^gists/add$', views.add_gist, name='add_gist'),
	url(r'^gists/(?P<gist_id>\d+)/remove$', views.remove_gist, name='remove_gist'),
	url(r'^login$', login, {'template_name':'users/login.html'}),
	url(r'^logout$', logout, {'next_page':'/'} ),
	url(r'^register$', views.register, name='register'),
)

