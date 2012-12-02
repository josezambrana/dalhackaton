# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from educacion.views import CreateCourse
from educacion.views import DetailCourse
from educacion.views import ListCourse
from educacion.views import EnrollView

from educacion.views import CreateProgram
from educacion.views import DetailProgram

from educacion.views import CreateLesson
from educacion.views import CreateResource
from educacion.views import CreateExam
from educacion.views import CreateQuestion
from educacion.views import CreateOption


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
    
    # Lecciones
    url(r'^lecciones/nuevo$', CreateLesson.as_view(), name="educacion_lessoncreate"),
    url(r'^recursos/nuevo$', CreateResource.as_view(), name="educacion_resourcecreate"),
    url(r'^recursos/nuevo\.(?P<format>html|json)$', CreateResource.as_view(), name="educacion_resourcecreate"),
    url(r'^examenes/nuevo', CreateExam.as_view(), name="educacion_examcreate"),
    url(r'^preguntas/nuevo', CreateQuestion.as_view(), name="educacion_questioncreate"),
    url(r'^opciones/nuevo', CreateOption.as_view(), name="educacion_optioncreate"),
)
