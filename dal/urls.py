from django.conf.urls import patterns, include, url
from django.conf import settings
from common.views import BaseView
from educacion.views import HomeView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^', include('common.urls')),
    url(r'^usuarios/', include('users.urls')),
    url(r'^social/', include('socialauth.urls')),
    url(r'edu/', include('educacion.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
