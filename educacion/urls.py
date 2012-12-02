# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from educacion.views import CreateCourse
from educacion.views import DetailCourse
from educacion.views import ListCourse
from educacion.views import EnrollView

from educacion.views import CreateProgram
from educacion.views import DetailProgram


urlpatterns = patterns('',
    # Courses
    url(r'^cursos$', ListCourse.as_view(), name='educacion_courselist'),
    url(r'^cursos/nuevo', CreateCourse.as_view(), name='educacion_coursecreate'),
    url(r'^cursos/(?P<pk>\d+)/inscribirse', EnrollView.as_view(), name='educacion_courseenroll'),
    url(r'^cursos/(?P<slug>[\w\-]+)$', DetailCourse.as_view(), name='educacion_courseshow'),
    
    url(r'^programas/(?P<program_slug>[\w\-]+)/cursos/nuevo', CreateCourse.as_view(), name='educacion_program_coursecreate'),

    # Programs
    url(r'^programas/nuevo', CreateProgram.as_view(), name="educacion_programcreate"),
    url(r'^programas/(?P<slug>[\w\-]+)$', DetailProgram.as_view(), name='educacion_programshow'),
)
