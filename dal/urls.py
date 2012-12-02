from django.conf.urls import patterns, include, url
from common.views import BaseView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', BaseView.as_view(app_name='dal', view_name='home'), name='home'),
    url(r'^', include('common.urls')),
    url(r'^usuarios/', include('users.urls')),
    url(r'^social/', include('socialauth.urls')),
    url(r'edu/', include('educacion.urls')),
)

