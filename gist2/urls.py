from django.conf.urls import patterns, url
from gist2 import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	url(r'^(?P<page>\d*)$', views.index, name='index'),
	url(r'^gists/(?P<gist_id>\d+)/$', views.detail_gist, name='detail_gist'),
	url(r'^users/(?P<pk>\d+)/$', views.DetailUserView.as_view(), name='detail_user'),
	url(r'^users/(?P<pk>\d+)/gists/$', views.UserGists.as_view(), name='user_gists'),
	url(r'^gists/(?P<gist_id>\d+)/edit$', views.edit_gist, name='edit_gist'),
	url(r'^login$', login, {'template_name':'users/login.html'}),
	url(r'^logout$', logout, {'next_page':'/'} ),
)

