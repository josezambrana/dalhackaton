# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from educacion.views import CreateCourse
from educacion.views import DetailCourse
from educacion.views import ListCourse

urlpatterns = patterns('',
    url(r'^$', ListCourse.as_view(), name='educacion_courselist'),
    url(r'nuevo_curso', CreateCourse.as_view(), name='educacion_coursecreate'),
    url(r'^(?P<slug>[\w\-]+)$', DetailCourse.as_view(), name='educacion_courseshow'),
)
