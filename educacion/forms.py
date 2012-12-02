# -*- coding: utf-8 -*-
import logging
from django import forms

from educacion.models import Course
from educacion.models import Program
from educacion.models import Lesson
from educacion.models import Resource
from educacion.models import Exam
from educacion.models import Question
from educacion.models import Option

logger = logging.getLogger('project.simple')


class WithOwnerMixin(object):
    """
    Modelo abstracto para contenidos que tienen propietario
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WithOwnerMixin, self).__init__(*args, **kwargs)

    def save(self):
        obj = super(WithOwnerMixin, self).save(commit=False)
        
        # Datos del autor
        obj.user = self.user
        obj.username = self.user.username
        obj.save()
        
        return obj


class CourseForm(WithOwnerMixin, forms.ModelForm):
    """
    Formulario para crear cursos
    """

    class Meta:
        model = Course 
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        self.program = kwargs.pop('program', None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def save(self):
        obj = super(CourseForm, self).save()
        
        obj.program = self.program
        obj.save()

        return obj


class ProgramForm(WithOwnerMixin, forms.ModelForm):
    """
    Formulario para gestionar Programas
    """

    class Meta:
        model = Program
        fields = ('name', 'description')


class LessonForm(WithOwnerMixin, forms.ModelForm):
    """
    Formulario para crear y editar Lecciones
    """
    
    class Meta:
        model = Lesson
        fields = ('description', 'orden', 'course')


MIMETYPES = {
    'video/x-flv': 'VIDEO',
    'application/pdf': 'DOC',
    'audio/mpeg': 'AUDIO'
}

class ResourceForm(forms.ModelForm):
    """
    Formulario para crear recursos para una lección.
    """
    
    class Meta:
        model = Resource
        fields = ('file', 'lesson')

    def clean_file(self):
        logger.info('***** ResourceForm.clean file')
        file = self.cleaned_data.get('file')

        logger.info('    * file.content_type: %s ' % file.content_type)
        if file.content_type not in MIMETYPES:
            raise forms.ValidationError(u'Archivo no permitido')

        self.type = MIMETYPES.get(file.content_type)
        logger.info('    * type: %s ' % self.type)
        return file

    def save(self):
        resource = super(ResourceForm, self).save(commit=False)
        resource.type = self.type
        resource.save()
        return resource

class ExamForm(forms.ModelForm):
    """
    Formulario para crear pruebas dentro de un recurso.
    """

    class Meta:
        model = Exam
        fields = ('resource', 'max_value', 'seconds')

class QuestionForm(forms.ModelForm):
    """
    Formulario para crear preguntas.
    """
    
    class Meta:
        model = Question
        fields = ('question', 'percent', 'exam', 'reply', 'explanation', 'weight')

class OptionForm(forms.ModelForm):
    """
    Formulario para crear opciones de respuesta para una pregunta.
    """

    class Meta:
        model = Option
        fields = ('value', 'correct', 'weight', 'question')
