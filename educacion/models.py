# -*- coding: utf-8 -*-
import logging
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from common.models import Content


logger = logging.getLogger('project.simple')


class Program(Content):
    """
    Un programa es una conjunto de cursos ordenados.
    """
    
    #: Propietario.
    username = models.CharField(_(u'Nombre de usuario'), max_length=255)

    #: Descripción del programa.
    description = models.TextField(_(u'Descripción'))

    class Meta:
        verbose_name = _(u'Programa')
        verbose_name_plural = _(u'Programas')
    
    @models.permalink
    def get_absolute_url(self):
        return ('educacion_programshow', [self.slug])



class Course(Content):
    """
    Un curso.
    """
    
    username = models.CharField(_(u'Nombre de usuario'), max_length=255)

    #: Descripción del curso
    description = models.TextField(_(u'Descripción'))

    #: Usuarios inscritos
    enrolled = models.ManyToManyField(User, related_name='courses')

    #: Programa al que pertenece
    program = models.ForeignKey(Program, verbose_name=_('Programa'), 
                                  related_name='courses', null=True)

    class Meta:
        verbose_name = _(u'Curso')
        verbose_name_plural = _(u'Cursos')
    
    def is_enrolled(self, user):
        return self.enrolled.filter(pk=user.id).exists()
    
    @models.permalink
    def get_absolute_url(self):
        return ('educacion_courseshow', [self.slug])


class Lesson(Content):
    """
    Una lección dentro de un curso.
    """

    #: Descripción del tema.
    description = models.TextField(_(u'Descripción'))

    #: Orden del tema
    orden = models.IntegerField(_(u'Orden'))

    #: Curso al que pertenece
    course = models.ForeignKey(Course, verbose_name=_(u'Curso'), 
                               related_name='Lessons')

    class Meta:
        verbose_name = _(u'Lección')
        verbose_name_plural = _(u'Lecciones')


RESOURCE_TYPES = (
    ('DOC', 'Document'),
    ('VIDEO', 'Video'),
    ('AUDIO', 'Audio'),
)

class Resource(models.Model):
    """
    Recurso video, pdf, doc, etc
    """
    
    #: Archivo del recurso
    file = models.FileField(upload_to='recursos', verbose_name=_(u'Archivo'))
    
    #: Tipo de Recurso
    type = models.CharField(max_length=5, choices=RESOURCE_TYPES, verbose_name=_(u'Tipo de recurso'))
    
    #: Lección a la que pertenece el recurso
    lesson = models.ForeignKey(Lesson, verbose_name=_(u'Lección'))

    class Meta:
        verbose_name = _(u'Recurso')
        verbose_name_plural = _(u'Recursos')

    def __unicode__(self):
        return unicode(self.file.url)
    

class Exam(models.Model):
    """
    Prueba para verificar una lección.
    """
    
    #: Recurso al que pertenece
    resource = models.ForeignKey(Resource, verbose_name=_(u'Recurso'), 
                                 related_name='exams')
    #: Máximo valor para la prueba
    max_value = models.IntegerField(_(u'Puntaje Máximo'), default=100)
    
    #: Muestra la prueba cuando se esta reproduciondo un video o audio
    seconds = models.IntegerField(_(u'Mostrar en'), null=True, blank=True)
    
    class Meta:
        verbose_name = _(u'Prueba')
        verbose_name_plural = _(u'Pruebas')
    
    def __unicode__(self):
        return unicode(u'Examen: %s ' % self.resource)

class Question(models.Model):
    """
    Pregunta realizada para una prueba
    """
    
    #: Prequnta que se hace
    question = models.CharField(max_length=512, verbose_name=_(u'Pregunta'))
    
    #: Porcentaje del examen
    percent = models.FloatField(_(u'Porcentaje'))

    #: Prueba a la que pertenece la pregunta
    exam = models.ForeignKey(Exam, verbose_name=_(u'Prueba'))
    
    #: Respuesta correcta
    reply = models.CharField(max_length=512, verbose_name=_(u'Respuesta correcta'))

    #: Explicacion
    explanation = models.TextField(_(u'Explicación'))
    
    #: Orden o peso
    weight = models.IntegerField(_(u'Orden en el que aparece'))
    
    class Meta:
        verbose_name = _(u'Pregunta')
        verbose_name_plural = _(u'Preguntas')


class Option(models.Model):
    """
    Opciones de respuesta para las preguntas.
    """
    
    #: Valor
    value = models.CharField(max_length=255, verbose_name=_(u'Valor'))
    
    #: Correcto
    correct = models.BooleanField(_(u'Correcto?'))
    
    #: Orden o peso
    weight = models.IntegerField(_(u'Peso'))

    #: Pregunta a la que pertenece
    question = models.ForeignKey(Question, verbose_name=_(u'Opción'))

    class Meta:
        verbose_name = _(u'Opción')
        verbose_name_plural = _(u'Opciones')
    
