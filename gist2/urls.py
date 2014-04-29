from django.conf.urls import patterns, url
from gist2 import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^gists/(?P<pk>\d+)/$', views.DetailGistView.as_view(), name='detail_gist'),
	url(r'^users/(?P<pk>\d+)/$', views.DetailUserView.as_view(), name='detail_user'),
	url(r'^users/(?P<pk>\d+)/gists/$', views.UserGists.as_view(), name='user_gists'),
	url(r'^gists/(?P<gist_id>\d+)/edit$', views.edit_gist, name='edit_gist'),
)

