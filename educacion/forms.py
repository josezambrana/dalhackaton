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
from educacion.models import Selection

logger = logging.getLogger('project.simple')


class WithOwnerMixin(object):
    """
    Modelo abstracto para contenidos que tienen propietario
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WithOwnerMixin, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
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
        fields = ('name', 'description', 'course', 'orden')


MIMETYPES = {
    'video/x-flv': 'VIDEO',
    'video/mpeg': 'VIDEO',
    'video/ogg': 'VIDEO',
    'video/x-theora+ogg': 'VIDEO',
    'video/mp4': 'VIDEO',
    'video/webm': 'VIDEO',
    'application/pdf': 'DOC',
    'audio/mpeg': 'AUDIO',
    'audio/ogg': 'AUDIO',
}

class ResourceForm(forms.ModelForm):
    """
    Formulario para crear recursos para una lección.
    """
    
    class Meta:
        model = Resource
        fields = ('name', 'file', 'lesson')

    def __init__(self, *args, **kwargs):
        logger.info("***** ResourceForm.__init__")
        self.user = kwargs.pop('user')
        return super(ResourceForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        logger.info("***** clean_file")
        file = self.cleaned_data.get('file')
        logger.info("    * file.content_type: %s " % file.content_type)
        if file.content_type not in MIMETYPES:
            raise forms.ValidationError(u'Archivo no permitido')

        self.type = MIMETYPES.get(file.content_type)
        self.mimetype = file.content_type
        return file

    def save(self):
        resource = super(ResourceForm, self).save(commit=False)
        logger.info("    * name: %s " % resource.name)
        logger.info("    * file: %s " % resource.file)
        resource.user = self.user
        logger.info("    * user: %s " % resource.user)
        resource.type = self.type
        logger.info("    * type: %s " % resource.type)
        resource.mimetype = self.mimetype
        logger.info("    * mimetype: %s " % resource.mimetype)
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

class SelectionForm(forms.ModelForm):
    """
    Formulario para seleccionar la respuesta a una pregunta
    """

    class Meta:
        model = Selection
        fields = ('question', 'opcion')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SelectionForm, self).__init__(*args, **kwargs)

    def save(self):
        selection = super(SelectionForm, self).save(commit=False)
        selection.exam = selection.question.exam
        selection.user = self.user
        selection.save()
        return selection

