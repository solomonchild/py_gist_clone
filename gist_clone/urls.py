from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gist_clone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('gist2.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
if not settings.DEBUG:
  urlpatterns += patterns('',
       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/media'})
   )
